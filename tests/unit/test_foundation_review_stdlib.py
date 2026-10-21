"""Independent synthetic boundary tests; no third-party modules or network required."""
import csv
import unittest
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal as D
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from gmrl.domain import (
    AccountState, Bar, CanonicalOrder, CorporateAction, CostModel,
    DatasetRequest, DividendReceivable, Fill, FXQuote, Instrument, JournalEntry,
    Lot, MarketData, OrderRequest, PaperState, Provenance, ProviderStatus,
    RatePolicy, RiskLimits, Session,
)
from gmrl.data.csv_import import import_bars_csv
from gmrl.data.subset import known_at
from gmrl.data.validation import validate_market_data
from gmrl.errors import (
    AccountingError, AuthenticationError, DataUnavailableError,
    DataValidationError, QuotaExceededError, TransientProviderError,
)
from gmrl.providers.cache import CachedProvider, FallbackProvider, canonical_request_key
from gmrl.storage.codec import dumps, loads
from gmrl.storage.repository import Repository

AT = datetime(2025, 1, 2, 9, tzinfo=timezone.utc)


def fixture():
    listing = Instrument('DEMO-X', 'Synthetic', None, 'DEMO', 'EUR', 'UTC',
                         'XX', 'equity', 'test', (), date(2025, 1, 1), None)
    bar = Bar('DEMO-X', AT.date(), AT, AT + timedelta(hours=7),
              AT + timedelta(hours=8), D(10), D(11), D(9), D(10), D(100), 'raw', 'p')
    provenance = Provenance('p', 'test', 'synthetic', AT, 'CC0', True, '0' * 64)
    return MarketData((listing,), (Session('DEMO-X', AT.date(), AT, bar.close_at),),
                      (bar,), (), (), (provenance,))


def state():
    account = AccountState(
        D('12.12345678901234567890123456'), (('DEMO-X', D('1.000001')),),
        (Lot('lot', 'DEMO-X', AT, D('1.000001'), D('10.000000000001')),),
        (DividendReceivable('a', 'DEMO-X', D('1.000001'), D('2.000002'),
                            'EUR', AT + timedelta(days=1)),))
    return PaperState(account, D(1000), 0, AT, ('a',))


def canonical():
    return CanonicalOrder(
        OrderRequest('PAPER-order', 'DEMO-X', 'buy', D(1), AT), '0' * 64,
        CostModel(*(D(0) for _ in range(5))),
        RiskLimits(D(1), D(1000), D('.1'), D(10), 96, 96))


class BoundaryReview(unittest.TestCase):
    def test_nonfinite_each_field_and_bad_chronology(self):
        data = fixture()
        for field in ('open', 'high', 'low', 'close', 'volume'):
            for bad in ('NaN', 'Infinity', '-Infinity'):
                with self.subTest(field=field, value=bad):
                    with self.assertRaises(DataValidationError):
                        validate_market_data(replace(data, bars=(replace(data.bars[0], **{field: D(bad)}),)))
        for bad in (replace(data.bars[0], instrument_id='unknown'),
                    replace(data.bars[0], available_at=AT),
                    replace(data.bars[0], volume=D(-1))):
            with self.assertRaises(DataValidationError):
                validate_market_data(replace(data, bars=(bad,)))

    def test_actions_and_fx_reject_future_knowledge(self):
        data = fixture()
        dividend = CorporateAction('a', 'DEMO-X', 'dividend', AT, AT, D(1), AT)
        split = CorporateAction('s', 'DEMO-X', 'split', AT, AT, D(2), None)
        for actions in ((dividend, dividend), (replace(dividend, available_at=AT + timedelta(seconds=1)),),
                        (dividend, split), (replace(split, amount=D('NaN')),)):
            with self.assertRaises(DataValidationError):
                validate_market_data(replace(data, actions=actions))
        validate_market_data(replace(data, actions=(replace(dividend, dividend_basis='post_split'), split)))
        for quote in (FXQuote('EUR', AT, AT, D(2), 'p'),
                      FXQuote('USD', AT, AT - timedelta(seconds=1), D(1), 'p')):
            with self.assertRaises(DataValidationError):
                validate_market_data(replace(data, fx=(quote,)))

    def test_history_physically_filters_delayed_and_future_values(self):
        data = fixture()
        early = AT + timedelta(hours=7, minutes=30)
        future_fx = FXQuote('EUR', early, early + timedelta(seconds=1), D(1), 'p')
        future_action = CorporateAction('a', 'DEMO-X', 'split', early, early, D(2), None)
        data = replace(data, fx=(future_fx,), actions=(future_action,))
        before = known_at(data, early - timedelta(seconds=1))
        self.assertEqual((before.bars, before.fx, before.actions), ((), (), ()))
        self.assertEqual(before, known_at(replace(data, bars=(replace(data.bars[0], high=D(999)),)), early - timedelta(seconds=1)))
        self.assertEqual(known_at(data, data.bars[0].available_at).bars, data.bars)

    def test_csv_offline_and_malformed_boundaries(self):
        data = fixture()
        columns = ('instrument_id', 'session_date', 'open_at', 'close_at',
                   'available_at', 'open', 'high', 'low', 'close', 'volume', 'price_basis')
        row = {k: str(getattr(data.bars[0], k)) for k in columns}
        with TemporaryDirectory() as folder, patch('socket.socket', side_effect=AssertionError('network forbidden')):
            target = Path(folder) / 'test.csv'
            cases = ({}, {'price_basis': ''}, {'open_at': '2025-01-02T09:00:00'},
                     {'close': 'NaN'}, {'instrument_id': 'unknown'})
            for changes in cases:
                with target.open('w', newline='', encoding='utf-8') as stream:
                    writer = csv.DictWriter(stream, fieldnames=columns)
                    writer.writeheader()
                    writer.writerow(row | changes)
                if not changes:
                    self.assertEqual(import_bars_csv(target, data.instruments, data.provenance[0]), data.bars)
                else:
                    with self.assertRaises(DataValidationError):
                        import_bars_csv(target, data.instruments, data.provenance[0])

    def test_unknown_timezone_rejects(self):
        data = fixture()
        with self.assertRaises(DataValidationError):
            validate_market_data(replace(data, instruments=(replace(data.instruments[0], timezone='Definitely/Invalid'),)))
    def test_wrong_session_date_rejects(self):
        data = fixture()
        wrong = AT.date() + timedelta(days=1)
        with self.assertRaises(DataValidationError):
            validate_market_data(replace(data, sessions=(replace(data.sessions[0], session_date=wrong),),
                                         bars=(replace(data.bars[0], session_date=wrong),)))


class PersistenceReview(unittest.TestCase):
    def test_lossless_all_nested_account_fields_and_offset(self):
        value = replace(state(), simulation_time=AT.astimezone(timezone(timedelta(hours=5, minutes=30))))
        self.assertEqual(loads(dumps(value)), value)
        with TemporaryDirectory() as folder:
            repo = Repository(Path(folder))
            with repo.paper_transaction() as tx:
                tx.save_account(value, expected_version=None)
            with Repository(Path(folder)).paper_transaction() as tx:
                self.assertEqual(tx.load_account(), value)

    def test_unknown_and_malformed_serialization_rejects(self):
        for payload in ('{"@":"NotARecord","v":{}}', '{"@":"datetime","v":"invalid"}',
                        '{"@":"PaperState","v":{}}', '{"@":"Decimal"}'):
            with self.subTest(payload=payload), self.assertRaises((ValueError, TypeError, KeyError, AttributeError)):
                loads(payload)

    def test_incomplete_account_must_not_silently_default_holdings_detail(self):
        payload = '{"@":"AccountState","v":{"cash_eur":{"@":"Decimal","v":"1"},"positions":{"@":"tuple","v":[]}}}'
        with self.assertRaises((ValueError, TypeError)):
            loads(payload)

    def test_atomic_rollback_includes_every_paper_record(self):
        order = canonical()
        fill = Fill('PAPER-fill', 'PAPER-order', 'DEMO-X', 'buy', D(1), AT, D(10), D(1), D(0), D(0))
        action = CorporateAction('a', 'DEMO-X', 'split', AT, AT, D(2), None)
        with TemporaryDirectory() as folder:
            repo = Repository(Path(folder))
            with self.assertRaises(KeyboardInterrupt):
                with repo.paper_transaction() as tx:
                    tx.save_account(state(), expected_version=None)
                    tx.append_order(order)
                    tx.append_fill('PAPER-order', fill)
                    tx.append_action(action)
                    tx.append_journal(JournalEntry('j', 'PAPER-order', 'test', 'test', AT))
                    raise KeyboardInterrupt('injected')
            with repo.paper_transaction() as tx:
                self.assertIsNone(tx.load_account())
                self.assertIsNone(tx.lookup_order('PAPER-order'))
                self.assertIsNone(tx.lookup_fill('PAPER-order'))
                self.assertIsNone(tx.lookup_action('a'))
                self.assertEqual(tx.journal(), ())

    def test_duplicate_identity_and_version_capital_time_guards(self):
        with TemporaryDirectory() as folder:
            repo = Repository(Path(folder))
            with repo.paper_transaction() as tx:
                tx.save_account(state(), expected_version=None)
            for value, expected in ((replace(state(), version=1), None),
                                    (replace(state(), version=2), 0),
                                    (replace(state(), version=1, initial_cash_eur=D(9)), 0),
                                    (replace(state(), version=1, simulation_time=AT-timedelta(seconds=1)), 0)):
                with self.assertRaises(AccountingError), repo.paper_transaction() as tx:
                    tx.save_account(value, expected_version=expected)
            def append(_):
                try:
                    with repo.paper_transaction() as tx:
                        tx.append_order(canonical())
                    return 1
                except AccountingError:
                    return 0
            with ThreadPoolExecutor(max_workers=2) as executor:
                self.assertEqual(sum(executor.map(append, range(2))), 1)
            with repo.paper_transaction() as tx:
                self.assertEqual(tx.lookup_order('PAPER-order'), canonical())


class Clock:
    def __init__(self):
        self.at = AT
        self.delays = []

    def now(self):
        return self.at

    def sleep(self, seconds):
        self.delays.append(seconds)
        self.at += timedelta(seconds=seconds)


class FakeRepository:
    """Cache boundary stub; intentionally does not pretend to verify Parquet."""
    root = Path('synthetic-cache-review')

    def __init__(self):
        self.cache = {}
        self.usage = []

    def cache_get(self, key):
        return self.cache.get(key)

    def cache_put(self, key, value):
        self.cache[key] = value

    def save_dataset(self, value):
        validate_market_data(value)
        return '0' * 64

    def record_usage(self, *args):
        self.usage.append(args)


class FakeProvider:
    def __init__(self, failures=(), quota=None):
        self.failures = list(failures)
        self.calls = 0
        self.quota = quota

    def status(self):
        return ProviderStatus('fake', True, 'synthetic', self.calls, self.quota)

    def fetch(self, request):
        self.calls += 1
        if self.failures:
            raise self.failures.pop(0)
        return fixture()


class CacheReview(unittest.TestCase):
    def setup_cache(self, provider):
        clock, repository = Clock(), FakeRepository()
        cache = CachedProvider(provider, repository, 60, clock=clock.now,
                               sleep=clock.sleep, random=lambda: .5,
                               rate_policy=RatePolicy(10, 1, 10))
        request = DatasetRequest(('DEMO-X',), AT.date(), AT.date())
        return cache, clock, repository, request

    def test_retry_after_attempt_bound_debits_and_ttl_boundary(self):
        provider = FakeProvider([TransientProviderError('test', 4), TransientProviderError('test')])
        cache, clock, repo, request = self.setup_cache(provider)
        result = cache.fetch(request)
        self.assertEqual((provider.calls, clock.delays, result.cache_status), (3, [4, 2], 'miss'))
        self.assertEqual(sum(row[3] for row in repo.usage), 3)
        self.assertEqual(cache.fetch(request).cache_status, 'hit')
        self.assertEqual(repo.usage[-1][3], 0)
        clock.sleep(60)
        self.assertEqual(cache.fetch(request).cache_status, 'miss')
        self.assertEqual(provider.calls, 4)

    def test_auth_validation_no_retry_and_three_failed_attempts(self):
        for exception in (AuthenticationError('test'), DataValidationError('test')):
            provider = FakeProvider([exception])
            cache, _, repo, request = self.setup_cache(provider)
            with self.assertRaises(type(exception)):
                cache.fetch(request)
            self.assertEqual((provider.calls, len(repo.usage)), (1, 1))
        provider = FakeProvider([TransientProviderError('test')] * 4)
        cache, _, _, request = self.setup_cache(provider)
        with self.assertRaises(DataUnavailableError):
            cache.fetch(request)
        self.assertEqual(provider.calls, 3)

    def test_cache_identity_and_stale_metadata(self):
        provider = FakeProvider()
        cache, clock, repo, request = self.setup_cache(provider)
        original = cache.fetch(request)
        clock.sleep(61)
        provider.failures = [TransientProviderError('test')] * 3
        stale = cache.fetch(request)
        self.assertEqual((stale.cache_status, stale.retrieved_at, stale.expires_at),
                         ('stale', original.retrieved_at, original.expires_at))
        self.assertTrue(stale.warnings)
        self.assertEqual(canonical_request_key('fake', replace(request, instrument_ids=('b', 'a', 'a'))),
                         canonical_request_key('fake', replace(request, instrument_ids=('a', 'b'))))
        self.assertNotEqual(canonical_request_key('other', request), canonical_request_key('fake', request))

    def test_expired_cache_remains_available_when_quota_exhausted(self):
        provider = FakeProvider()
        cache, clock, _, request = self.setup_cache(provider)
        cache.fetch(request)
        clock.sleep(61)
        provider.quota = 0
        self.assertEqual(cache.fetch(request).cache_status, 'stale')
        self.assertEqual(provider.calls, 1)

    def test_quota_rechecked_before_each_retry(self):
        class ExhaustingProvider(FakeProvider):
            def fetch(self, request):
                self.calls += 1
                self.quota = 0
                raise TransientProviderError('last permitted attempt failed')
        provider = ExhaustingProvider(quota=1)
        cache, _, _, request = self.setup_cache(provider)
        with self.assertRaises((QuotaExceededError, DataUnavailableError)):
            cache.fetch(request)
        self.assertEqual(provider.calls, 1)

    def test_token_wait_bound_and_same_request_coalescing(self):
        provider = FakeProvider()
        cache, clock, _, request = self.setup_cache(provider)
        with ThreadPoolExecutor(max_workers=2) as executor:
            results = tuple(executor.map(cache.fetch, (request, request)))
        self.assertEqual(provider.calls, 1)
        self.assertEqual(sorted(result.cache_status for result in results), ['hit', 'miss'])
        cache.tokens = 0
        cache.policy = RatePolicy(1, .01, 1)
        with self.assertRaises(QuotaExceededError):
            cache.fetch(replace(request, end=request.end + timedelta(days=1)))
        self.assertEqual(clock.delays, [])
        self.assertEqual(provider.calls, 1)

    def test_fallback_preserves_order_and_does_not_hide_validation(self):
        first = FakeProvider([DataUnavailableError('offline')])
        second = FakeProvider()
        request = DatasetRequest(('DEMO-X',), AT.date(), AT.date())
        self.assertEqual(FallbackProvider((first, second)).fetch(request), fixture())
        self.assertEqual((first.calls, second.calls), (1, 1))
        first = FakeProvider([DataValidationError('bad data')])
        with self.assertRaises(DataValidationError):
            FallbackProvider((first, second)).fetch(request)
        self.assertEqual(second.calls, 1)


if __name__ == '__main__':
    unittest.main()
