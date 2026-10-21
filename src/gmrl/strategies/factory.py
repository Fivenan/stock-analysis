"""Three stateless strategies; scheduling belongs to the engine."""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from gmrl.data.subset import known_at
from gmrl.domain import MarketData, TargetWeights
from gmrl.errors import DataValidationError
from gmrl.strategies.base import Strategy


def signal_series(history: MarketData, ident: str, at: datetime, *,
                  total_return: bool = False) -> list[Decimal]:
    """Point-in-time split-normalized closes or a local dividend-return index."""
    data = known_at(history, at)
    bars = sorted((b for b in data.bars if b.instrument_id == ident), key=lambda b: b.close_at)
    if not bars:
        return []
    observed = {b.session_date for b in bars}
    if any(s.session_date not in observed for s in data.sessions
           if s.instrument_id == ident and bars[0].session_date <= s.session_date <= bars[-1].session_date):
        raise DataValidationError("Signal history has an expected-session outage")
    actions = [a for a in data.actions if a.instrument_id == ident]
    if not total_return:
        values = []
        for bar in bars:
            ratio = Decimal(1)
            for action in actions:
                if action.kind == "split" and bar.close_at < action.effective_at <= bars[-1].close_at:
                    ratio *= action.amount
            values.append(bar.close / ratio)
        return values
    values = [Decimal(1)]
    for previous, current in zip(bars, bars[1:]):
        shares = Decimal(1)
        cash = Decimal(0)
        between = sorted((a for a in actions if previous.close_at < a.effective_at <= current.close_at),
                         key=lambda a: (a.effective_at, a.kind == "split", a.action_id))
        for action in between:
            if action.kind == "split":
                shares *= action.amount
            else:
                entitlement = shares
                if action.dividend_basis == "post_split":
                    for split in between:
                        if split.kind == "split" and split.effective_at == action.effective_at:
                            entitlement *= split.amount
                cash += entitlement * action.amount
        # Local gross return index assumes dividend reinvestment at the completed close.
        values.append(values[-1] * (current.close * shares + cash) / previous.close)
    return values


@dataclass(frozen=True, slots=True)
class ResearchStrategy:
    name: str
    lookback: int = 60
    top_n: int = 3

    @property
    def rebalance(self) -> str:
        return "once" if self.name == "buy_hold" else "monthly"

    def weights(self, history: MarketData, decided_at: datetime) -> TargetWeights:
        history = known_at(history, decided_at)
        scores: list[tuple[str, Decimal]] = []
        for listing in sorted(history.instruments, key=lambda i: i.instrument_id):
            if (listing.available_from > decided_at.date()
                    or listing.available_until and listing.available_until < decided_at.date()):
                continue
            series = signal_series(history, listing.instrument_id, decided_at,
                                   total_return=self.name == "momentum")
            if not series:
                continue
            if self.name == "buy_hold":
                scores.append((listing.instrument_id, Decimal(1)))
            elif self.name == "trend" and len(series) >= self.lookback:
                # Decimal arithmetic keeps equality stable across a neutral split.
                sma = sum(series[-self.lookback:], Decimal(0)) / self.lookback
                if series[-1] > sma:
                    scores.append((listing.instrument_id, series[-1] / sma - 1))
            elif self.name == "momentum" and len(series) >= self.lookback + 1:
                momentum = series[-1] / series[-self.lookback - 1] - 1
                if momentum > 0:
                    scores.append((listing.instrument_id, momentum))
        if self.name == "momentum":
            scores = sorted(scores, key=lambda pair: (-pair[1], pair[0]))[:self.top_n]
        if not scores:
            return TargetWeights(decided_at, ())
        weight = Decimal(1) / len(scores)
        # Decimal 1/3 can round upward in aggregate; never exceed one.
        weight = weight.quantize(Decimal("0.000000000001"), rounding="ROUND_DOWN")
        return TargetWeights(decided_at, tuple(sorted((ident, weight) for ident, _ in scores)))


def make_strategy(name: str, parameters: dict[str, int | float]) -> Strategy:
    if name not in ("buy_hold", "trend", "momentum"):
        raise DataValidationError("Implemented strategies: buy_hold, trend, momentum")
    if set(parameters) - {"lookback", "top_n"}:
        raise DataValidationError("Unknown strategy parameter")
    lookback = parameters.get("lookback", 60)
    top_n = parameters.get("top_n", 3)
    if int(lookback) != lookback or int(top_n) != top_n or lookback < 2 or top_n < 1:
        raise DataValidationError("Integer lookback >= 2 and top_n >= 1 required")
    return ResearchStrategy(name, int(lookback), int(top_n))
