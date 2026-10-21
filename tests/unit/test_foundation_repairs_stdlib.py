"""Regression coverage for persistence corruption and blocked refresh."""

import json
import unittest
from datetime import datetime, date, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from gmrl.domain import AccountState, DatasetRequest, MarketData, ProviderStatus, RatePolicy
from gmrl.storage.codec import dumps, loads
from gmrl.providers.cache import CachedProvider


class RepairRegressionTests(unittest.TestCase):
    def test_exact_complete_payload_fields(self):
        original = json.loads(dumps(AccountState(Decimal(1), ())))
        for field in original["v"]:
            altered = json.loads(json.dumps(original))
            del altered["v"][field]
            with self.subTest(missing=field), self.assertRaises(ValueError):
                loads(json.dumps(altered))
        original["v"]["unknown"] = 1
        with self.assertRaises(ValueError):
            loads(json.dumps(original))
        with self.assertRaises(ValueError):
            loads('{"@":"UnrecognizedRecord","v":{}}')

    def test_token_block_returns_stale_without_refresh_or_debit(self):
        class Provider:
            calls = 0

            def status(self):
                return ProviderStatus("test", True, "synthetic", self.calls, None)

            def fetch(self, request):
                self.calls += 1
                return MarketData((), (), (), (), (), ())

        class MemoryRepository:
            root = Path("synthetic-token-repair")
            saved = None
            usage = None

            def cache_get(self, key):
                return self.saved

            def cache_put(self, key, value):
                self.saved = value

            def save_dataset(self, value):
                return "0" * 64

            def record_usage(self, *args):
                self.usage = args

        at = [datetime(2025, 1, 1, tzinfo=timezone.utc)]
        provider, repository = Provider(), MemoryRepository()
        cache = CachedProvider(
            provider,
            repository,
            1,
            clock=lambda: at[0],
            sleep=lambda seconds: None,
            random=lambda: 0.5,
            rate_policy=RatePolicy(1, 0.001, 0),
        )
        request = DatasetRequest((), date(2025, 1, 1), date(2025, 1, 1))
        original = cache.fetch(request)
        at[0] += timedelta(seconds=2)
        stale = cache.fetch(request)
        self.assertEqual(stale.cache_status, "stale")
        self.assertEqual(
            (stale.retrieved_at, stale.expires_at), (original.retrieved_at, original.expires_at)
        )
        self.assertTrue(stale.warnings)
        self.assertEqual(provider.calls, 1)
        self.assertEqual(repository.usage[-2:], ("refresh_blocked", 0))


class ReadAPIRegressionTests(unittest.TestCase):
    def test_paper_enumerations_and_experiment_manifests(self):
        from tempfile import TemporaryDirectory
        from dataclasses import replace
        from gmrl.storage.repository import Repository
        from gmrl.domain import (
            CanonicalOrder,
            OrderRequest,
            CostModel,
            RiskLimits,
            Fill,
            CorporateAction,
        )
        from gmrl.errors import DataUnavailableError

        at = datetime(2025, 1, 1, tzinfo=timezone.utc)
        costs = CostModel(*(Decimal(0) for _ in range(5)))
        limits = RiskLimits(Decimal(1), Decimal(1000), Decimal(".1"), Decimal(10), 96, 96)
        first = CanonicalOrder(
            OrderRequest("PAPER-a", "DEMO-X", "buy", Decimal(1), at), "0" * 64, costs, limits
        )
        second = replace(first, order=replace(first.order, client_order_id="PAPER-z"))
        first_fill = Fill(
            "PAPER-fill-a",
            "PAPER-a",
            "DEMO-X",
            "buy",
            Decimal(1),
            at,
            Decimal(10),
            Decimal(1),
            Decimal(0),
            Decimal(0),
        )
        second_fill = replace(first_fill, fill_id="PAPER-fill-z", order_id="PAPER-z")
        first_action = CorporateAction("action-a", "DEMO-X", "split", at, at, Decimal(2), None)
        second_action = replace(first_action, action_id="action-z")
        with TemporaryDirectory() as directory:
            repository = Repository(Path(directory))
            with repository.paper_transaction() as tx:
                self.assertEqual((tx.orders(), tx.fills(), tx.actions()), ((), (), ()))
                for order, fill, action in (
                    (second, second_fill, second_action),
                    (first, first_fill, first_action),
                ):
                    tx.append_order(order)
                    tx.append_fill(order.order.client_order_id, fill)
                    tx.append_action(action)
                self.assertEqual(tx.orders(), (first, second))
                self.assertEqual(tx.fills(), (first_fill, second_fill))
                self.assertEqual(tx.actions(), (first_action, second_action))
            manifests = (
                {"strategy": "trend", "capital": Decimal("123.456789")},
                {"strategy": "buy_hold"},
            )
            ids = tuple(repository.save_experiment(manifest) for manifest in manifests)
            restarted = Repository(Path(directory))
            self.assertEqual(
                restarted.list_experiments(),
                tuple(manifest for key, manifest in sorted(zip(ids, manifests))),
            )
            for key, manifest in zip(ids, manifests):
                self.assertEqual(restarted.load_experiment(key), manifest)
            with self.assertRaises(DataUnavailableError):
                restarted.load_experiment("missing")
            with restarted.paper_transaction() as tx:
                self.assertEqual(tx.orders(), (first, second))
                self.assertEqual(tx.fills(), (first_fill, second_fill))
                self.assertEqual(tx.actions(), (first_action, second_action))


if __name__ == "__main__":
    unittest.main()
