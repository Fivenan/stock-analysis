"""No third-party dependencies; runnable with unittest before package approval."""

import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from dataclasses import replace
from concurrent.futures import ThreadPoolExecutor
from gmrl.domain import (
    AccountState,
    PaperState,
    JournalEntry,
    Instrument,
    Bar,
    Session,
    Provenance,
    MarketData,
    CorporateAction,
    FXQuote,
)
from gmrl.data.validation import validate_market_data
from gmrl.storage.repository import Repository
from gmrl.storage.codec import dumps, loads
from gmrl.errors import AccountingError, DataValidationError


class FoundationStdlibTests(unittest.TestCase):
    def test_decimal_codec(self):
        value = PaperState(
            AccountState(Decimal("0.1234567890123456789012345678"), ()),
            Decimal(1000),
            0,
            datetime(2025, 1, 1, tzinfo=timezone.utc),
            (),
        )
        self.assertEqual(loads(dumps(value)), value)

    def test_rollback_concurrency_restart(self):
        with TemporaryDirectory() as temp:
            repo = Repository(Path(temp))
            value = PaperState(
                AccountState(Decimal("123.456789012345678901"), ()),
                Decimal(1000),
                0,
                datetime(2025, 1, 1, tzinfo=timezone.utc),
                (),
            )
            with self.assertRaises(RuntimeError):
                with repo.paper_transaction() as tx:
                    tx.save_account(value, expected_version=None)
                    tx.append_journal(
                        JournalEntry("j", None, "hypothesis", "lesson", value.simulation_time)
                    )
                    raise RuntimeError("Crash injection")
            with repo.paper_transaction() as tx:
                self.assertIsNone(tx.load_account())
                self.assertEqual(tx.journal(), ())
                tx.save_account(value, expected_version=None)

            def update(_):
                try:
                    with repo.paper_transaction() as tx:
                        tx.save_account(replace(value, version=1), expected_version=0)
                    return 1
                except AccountingError:
                    return 0

            with ThreadPoolExecutor(max_workers=2) as pool:
                self.assertEqual(sum(pool.map(update, range(2))), 1)
            with Repository(Path(temp)).paper_transaction() as tx:
                self.assertEqual(tx.load_account(), replace(value, version=1))

    def test_validation(self):
        at = datetime(2025, 1, 2, 9, tzinfo=timezone.utc)
        instrument = Instrument(
            "DEMO-X",
            "Synthetic",
            None,
            "DEMO",
            "EUR",
            "UTC",
            "XX",
            "equity",
            "test",
            (),
            date(2025, 1, 1),
            None,
        )
        provenance = Provenance("p", "test", "synthetic", at, "CC0", True, "0" * 64)
        bar = Bar(
            "DEMO-X",
            at.date(),
            at,
            at + timedelta(hours=7),
            at + timedelta(hours=7),
            Decimal(10),
            Decimal(11),
            Decimal(9),
            Decimal(10),
            Decimal(100),
            "raw",
            "p",
        )
        data = MarketData(
            (instrument,),
            (Session("DEMO-X", at.date(), bar.open_at, bar.close_at),),
            (bar,),
            (),
            (),
            (provenance,),
        )
        validate_market_data(data)
        for bad in (
            replace(bar, volume=Decimal("NaN")),
            replace(bar, high=Decimal(1)),
            replace(bar, open_at=at.replace(tzinfo=None)),
            replace(bar, price_basis="adjusted"),
        ):
            with self.assertRaises(DataValidationError):
                validate_market_data(replace(data, bars=(bad,)))
        with self.assertRaises(DataValidationError):
            validate_market_data(replace(data, bars=(bar, bar)))
        action = CorporateAction("a", "DEMO-X", "dividend", at, at, Decimal(1), None)
        with self.assertRaises(DataValidationError):
            validate_market_data(replace(data, actions=(action,)))
        quote = FXQuote("EUR", at, at, Decimal("0.5"), "p")
        with self.assertRaises(DataValidationError):
            validate_market_data(replace(data, fx=(quote,)))


if __name__ == "__main__":
    unittest.main()
