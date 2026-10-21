from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    import pandas as pd


@dataclass(frozen=True, slots=True)
class Instrument:
    instrument_id: str
    name: str
    isin: str | None
    mic: str
    currency: str
    timezone: str
    country: str
    asset_class: str
    sector: str
    provider_symbols: tuple[tuple[str, str], ...]
    available_from: date
    available_until: date | None


@dataclass(frozen=True, slots=True)
class Session:
    instrument_id: str
    session_date: date
    open_at: datetime
    close_at: datetime


@dataclass(frozen=True, slots=True)
class Bar:
    instrument_id: str
    session_date: date
    open_at: datetime
    close_at: datetime
    available_at: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    price_basis: Literal["raw"]
    provenance_id: str


@dataclass(frozen=True, slots=True)
class CorporateAction:
    action_id: str
    instrument_id: str
    kind: Literal["dividend", "split"]
    effective_at: datetime
    available_at: datetime
    amount: Decimal
    pay_at: datetime | None
    dividend_basis: Literal["pre_split", "post_split"] | None = None


@dataclass(frozen=True, slots=True)
class FXQuote:
    currency: str
    observed_at: datetime
    available_at: datetime
    eur_per_unit: Decimal
    provenance_id: str


@dataclass(frozen=True, slots=True)
class Provenance:
    provenance_id: str
    provider: str
    source: str
    retrieved_at: datetime
    license_note: str
    synthetic: bool
    content_sha256: str


@dataclass(frozen=True, slots=True)
class MarketData:
    instruments: tuple[Instrument, ...]
    sessions: tuple[Session, ...]
    bars: tuple[Bar, ...]
    actions: tuple[CorporateAction, ...]
    fx: tuple[FXQuote, ...]
    provenance: tuple[Provenance, ...]


@dataclass(frozen=True, slots=True)
class DatasetRequest:
    instrument_ids: tuple[str, ...]
    start: date
    end: date


@dataclass(frozen=True, slots=True)
class CacheResult:
    data: MarketData
    dataset_id: str
    retrieved_at: datetime
    expires_at: datetime
    cache_status: Literal["hit", "miss", "stale"]
    warnings: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RatePolicy:
    capacity: int
    refill_per_second: float
    max_delay_seconds: float


@dataclass(frozen=True, slots=True)
class OpeningEvent:
    instrument_id: str
    at: datetime
    price_local: Decimal
    fx: FXQuote
    prior_volume: Decimal


@dataclass(frozen=True, slots=True)
class ProviderStatus:
    provider: str
    enabled: bool
    message: str
    used_requests: int
    quota_remaining: int | None


@dataclass(frozen=True, slots=True)
class TargetWeights:
    decided_at: datetime
    weights: tuple[tuple[str, Decimal], ...]


@dataclass(frozen=True, slots=True)
class CostModel:
    fixed_fee_eur: Decimal
    commission_bps: Decimal
    spread_bps: Decimal
    slippage_bps: Decimal
    fx_fee_bps: Decimal


@dataclass(frozen=True, slots=True)
class RiskLimits:
    max_weight: Decimal
    max_order_eur: Decimal
    max_volume_fraction: Decimal
    max_spread_bps: Decimal
    max_price_age_hours: int
    max_fx_age_hours: int


@dataclass(frozen=True, slots=True)
class BacktestConfig:
    initial_cash_eur: Decimal
    start: date
    end: date
    costs: CostModel
    limits: RiskLimits
    whole_shares: bool


@dataclass(frozen=True, slots=True)
class OrderRequest:
    client_order_id: str
    instrument_id: str
    side: Literal["buy", "sell"]
    quantity: Decimal
    submitted_at: datetime


@dataclass(frozen=True, slots=True)
class Fill:
    fill_id: str
    order_id: str
    instrument_id: str
    side: str
    quantity: Decimal
    filled_at: datetime
    price_local: Decimal
    fx_eur_per_unit: Decimal
    fee_eur: Decimal
    fx_cost_eur: Decimal


@dataclass(frozen=True, slots=True)
class Lot:
    lot_id: str
    instrument_id: str
    acquired_at: datetime
    quantity: Decimal
    total_basis_eur: Decimal


@dataclass(frozen=True, slots=True)
class DividendReceivable:
    action_id: str
    instrument_id: str
    quantity_entitled: Decimal
    amount_local: Decimal
    currency: str
    pay_at: datetime


@dataclass(frozen=True, slots=True)
class AccountState:
    cash_eur: Decimal
    positions: tuple[tuple[str, Decimal], ...]
    lots: tuple[Lot, ...] = ()
    receivables: tuple[DividendReceivable, ...] = ()


@dataclass(frozen=True, slots=True)
class RealizedMatch:
    instrument_id: str
    acquired_at: datetime
    disposed_at: datetime
    quantity: Decimal
    allocated_basis_eur: Decimal
    net_proceeds_eur: Decimal
    pnl_eur: Decimal


@dataclass(frozen=True, slots=True)
class LedgerResult:
    state: AccountState
    realized_matches: tuple[RealizedMatch, ...]


@dataclass(frozen=True, slots=True)
class PaperState:
    account: AccountState
    initial_cash_eur: Decimal
    version: int
    simulation_time: datetime
    processed_action_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CanonicalOrder:
    order: OrderRequest
    dataset_id: str
    costs: CostModel
    limits: RiskLimits


@dataclass(frozen=True, slots=True)
class JournalEntry:
    entry_id: str
    order_id: str | None
    hypothesis: str
    lesson: str
    recorded_at: datetime


@dataclass(frozen=True, slots=True)
class ValidationResult:
    accepted: bool
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class BacktestResult:
    equity: pd.DataFrame
    fills: tuple[Fill, ...]
    realized_matches: tuple[RealizedMatch, ...]
    metrics: dict[str, float | None]
    warnings: tuple[str, ...]
    experiment_id: str
