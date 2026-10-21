from datetime import datetime, timezone, tzinfo
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from gmrl.domain import MarketData, Session
from gmrl.errors import DataValidationError


def aware(value: datetime) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise DataValidationError("Timestamp must include a timezone offset")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise DataValidationError(message)


def validate_market_data(data: MarketData) -> None:
    ids = {i.instrument_id for i in data.instruments}
    require(len(ids) == len(data.instruments), "Duplicate instrument identity")
    instruments = {i.instrument_id: i for i in data.instruments}
    zones: dict[str, tzinfo] = {}
    for i in data.instruments:
        require(
            bool(i.instrument_id) and len(i.currency) == 3 and bool(i.timezone),
            "Invalid listing registry",
        )
        require(
            i.available_until is None or i.available_until >= i.available_from,
            "Invalid listing availability",
        )
        try:
            zones[i.instrument_id] = timezone.utc if i.timezone == "UTC" else ZoneInfo(i.timezone)
        except (ZoneInfoNotFoundError, ValueError) as exc:
            raise DataValidationError(
                "Listing timezone unavailable or unknown; install the approved timezone database for IANA zones"
            ) from exc
    prov = {p.provenance_id for p in data.provenance}
    require(len(prov) == len(data.provenance), "Duplicate provenance")
    for p in data.provenance:
        aware(p.retrieved_at)
        require(
            len(p.content_sha256) == 64
            and all((c in "0123456789abcdef" for c in p.content_sha256)),
            "Invalid provenance SHA256",
        )
    sessions = {}
    for s in data.sessions:
        aware(s.open_at)
        aware(s.close_at)
        key = (s.instrument_id, s.session_date)
        require(
            s.instrument_id in ids and key not in sessions and (s.open_at < s.close_at),
            "Invalid/duplicate session",
        )
        listing = instruments[s.instrument_id]
        require(
            s.open_at.astimezone(zones[s.instrument_id]).date() == s.session_date,
            "Session date differs from local opening date",
        )
        require(
            listing.available_from <= s.session_date
            and (listing.available_until is None or s.session_date <= listing.available_until),
            "Session outside listing availability",
        )
        sessions[key] = s
    seen = set()
    for b in data.bars:
        for t in (b.open_at, b.close_at, b.available_at):
            aware(t)
        key = (b.instrument_id, b.session_date)
        require(key not in seen and key in sessions, "Duplicate bar or unknown session")
        seen.add(key)
        s = sessions[key]
        require(
            b.open_at == s.open_at and b.close_at == s.close_at and (b.available_at >= b.close_at),
            "Invalid bar chronology",
        )
        require(
            b.price_basis == "raw" and b.provenance_id in prov,
            "Raw basis and known provenance required",
        )
        require(
            all((v.is_finite() for v in (b.open, b.high, b.low, b.close, b.volume))),
            "Nonfinite bar",
        )
        require(
            0 < b.low <= min(b.open, b.close) <= max(b.open, b.close) <= b.high and b.volume >= 0,
            "Invalid OHLC/volume",
        )
    action_ids = set()
    for a in data.actions:
        aware(a.effective_at)
        aware(a.available_at)
        require(
            a.action_id not in action_ids and a.instrument_id in ids, "Duplicate/unknown action"
        )
        action_ids.add(a.action_id)
        require(
            a.kind in ("dividend", "split")
            and a.amount.is_finite()
            and (a.amount > 0)
            and (a.available_at <= a.effective_at),
            "Invalid/late-known action",
        )
        if a.kind == "dividend":
            if a.pay_at is None:
                raise DataValidationError("Dividend payment date required")
            aware(a.pay_at)
            require(a.pay_at >= a.effective_at, "Payment precedes entitlement")
        if any(
            (
                x.kind != a.kind
                and x.instrument_id == a.instrument_id
                and (x.effective_at == a.effective_at)
                for x in data.actions
            )
        ):
            dividend = (
                a
                if a.kind == "dividend"
                else next(
                    (
                        x
                        for x in data.actions
                        if x.kind == "dividend"
                        and x.instrument_id == a.instrument_id
                        and (x.effective_at == a.effective_at)
                    )
                )
            )
            require(
                dividend.dividend_basis in ("pre_split", "post_split"),
                "Ambiguous simultaneous actions",
            )
    fx_seen = set()
    for q in data.fx:
        aware(q.observed_at)
        aware(q.available_at)
        fx_key = (q.currency, q.observed_at, q.available_at)
        require(fx_key not in fx_seen, "Duplicate FX")
        fx_seen.add(fx_key)
        require(
            q.eur_per_unit.is_finite()
            and q.eur_per_unit > 0
            and (q.available_at >= q.observed_at)
            and (q.provenance_id in prov),
            "Invalid FX/availability",
        )
        require(q.currency != "EUR" or q.eur_per_unit == 1, "EUR FX must equal one")


def session_gaps(data: MarketData) -> tuple[Session, ...]:
    observed = {(b.instrument_id, b.session_date) for b in data.bars}
    return tuple((s for s in data.sessions if (s.instrument_id, s.session_date) not in observed))
