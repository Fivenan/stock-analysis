from __future__ import annotations
from datetime import timedelta
from hashlib import sha256
from threading import RLock
from gmrl.domain import (
    CacheResult,
    DatasetRequest,
    RatePolicy,
    MarketData,
    Instrument,
    ProviderStatus,
)
from gmrl.providers.base import DataProvider
from gmrl.storage.repository import Repository
from datetime import datetime
from typing import Callable, Any
from gmrl.errors import (
    DataValidationError,
    DataUnavailableError,
    QuotaExceededError,
    TransientProviderError,
)
from gmrl.storage.codec import dumps

_LOCKS: dict[tuple[str, str], Any] = {}
_LOCKS_GUARD = RLock()


def canonical_request_key(provider: str, request: DatasetRequest) -> str:
    if request.start > request.end:
        raise DataValidationError("Start exceeds end")
    return sha256(
        dumps(
            (
                provider,
                tuple(sorted(set(request.instrument_ids))),
                "1d",
                request.start,
                request.end,
                "raw+actions",
                1,
            )
        ).encode()
    ).hexdigest()


class CachedProvider:
    def __init__(
        self,
        provider: DataProvider,
        repository: Repository,
        ttl_seconds: int,
        *,
        clock: Callable[[], datetime],
        sleep: Callable[[float], None],
        random: Callable[[], float],
        rate_policy: RatePolicy,
        max_attempts: int = 3,
    ) -> None:
        if (
            ttl_seconds < 0
            or not 1 <= max_attempts <= 3
            or rate_policy.capacity < 1
            or (rate_policy.refill_per_second <= 0)
            or (rate_policy.max_delay_seconds < 0)
        ):
            raise DataValidationError("Invalid cache/rate/retry policy")
        self.provider = provider
        self.repository = repository
        self.ttl = ttl_seconds
        self.clock = clock
        self.sleep = sleep
        self.random = random
        self.policy = rate_policy
        self.attempts = max_attempts
        self.tokens = float(rate_policy.capacity)
        self.updated = clock()
        self._bucket_lock = RLock()

    def _token(self) -> None:
        with self._bucket_lock:
            now = self.clock()
            self.tokens = min(
                self.policy.capacity,
                self.tokens
                + max(0, (now - self.updated).total_seconds()) * self.policy.refill_per_second,
            )
            self.updated = now
            delay = max(0, (1 - self.tokens) / self.policy.refill_per_second)
            if delay > self.policy.max_delay_seconds:
                raise QuotaExceededError("Token bucket wait exceeds policy")
            if delay:
                self.sleep(delay)
                self.updated = self.clock()
                self.tokens = 1
            self.tokens -= 1

    def fetch(self, request: DatasetRequest) -> CacheResult:
        provider = self.provider.status().provider
        key = canonical_request_key(provider, request)
        lock_key = (str(self.repository.root.resolve()), key)
        with _LOCKS_GUARD:
            lock = _LOCKS.setdefault(lock_key, RLock())
        with lock:
            cached = self.repository.cache_get(key)
            now = self.clock()
            if cached and now < cached.expires_at:
                self.repository.record_usage(provider, now, "cache_hit", 0)
                return CacheResult(
                    cached.data,
                    cached.dataset_id,
                    cached.retrieved_at,
                    cached.expires_at,
                    "hit",
                    cached.warnings,
                )
            failure = None
            for attempt in range(self.attempts):
                try:
                    remaining = self.provider.status().quota_remaining
                    if remaining is not None and remaining <= 0:
                        raise QuotaExceededError("Provider reports exhausted quota")
                    self._token()
                except QuotaExceededError as exc:
                    self.repository.record_usage(provider, self.clock(), "refresh_blocked", 0)
                    if cached:
                        return self._stale(cached, str(exc))
                    raise
                try:
                    data = self.provider.fetch(request)
                    dataset_id = self.repository.save_dataset(data)
                    at = self.clock()
                    result = CacheResult(
                        data, dataset_id, at, at + timedelta(seconds=self.ttl), "miss", ()
                    )
                    self.repository.cache_put(key, result)
                    self.repository.record_usage(provider, at, "success", 1)
                    return result
                except TransientProviderError as exc:
                    self.repository.record_usage(provider, self.clock(), "failure", 1)
                    failure = exc
                    if attempt + 1 < self.attempts:
                        delay = max(exc.retry_after, 2**attempt * (0.5 + self.random()))
                        if delay > self.policy.max_delay_seconds:
                            break
                        self.sleep(delay)
                except Exception:
                    self.repository.record_usage(provider, self.clock(), "failure", 1)
                    raise
            if cached:
                return self._stale(cached, "Refresh failed within bounded attempt policy")
            raise DataUnavailableError("Provider failed within bounded attempt policy") from failure

    @staticmethod
    def _stale(cached: CacheResult, reason: str) -> CacheResult:
        return CacheResult(
            cached.data,
            cached.dataset_id,
            cached.retrieved_at,
            cached.expires_at,
            "stale",
            cached.warnings
            + (reason + "; stale data is for research only and cannot authorize fills",),
        )


class FallbackProvider:
    """Explicit ordered raw-data adapters. No merging or provenance substitution."""

    def __init__(self, providers: tuple[DataProvider, ...]) -> None:
        if not providers:
            raise DataValidationError("Fallback list cannot be empty")
        self.providers = tuple(providers)

    def instruments(self) -> tuple[Instrument, ...]:
        return self.providers[0].instruments()

    def status(self) -> ProviderStatus:
        return self.providers[0].status()

    def fetch(self, request: DatasetRequest) -> MarketData:
        for provider in self.providers:
            try:
                return provider.fetch(request)
            except DataUnavailableError:
                continue
        raise DataUnavailableError("All explicitly configured compatible providers failed")
