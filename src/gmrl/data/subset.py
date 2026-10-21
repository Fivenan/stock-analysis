from datetime import datetime
from gmrl.domain import MarketData, DatasetRequest
from gmrl.errors import DataValidationError


def subset(data: MarketData, request: DatasetRequest) -> MarketData:
    ids = set(request.instrument_ids)
    if request.start > request.end or not ids.issubset({i.instrument_id for i in data.instruments}):
        raise DataValidationError("Invalid date bounds or instrument ID")
    return MarketData(
        tuple((i for i in data.instruments if i.instrument_id in ids)),
        tuple(
            (
                s
                for s in data.sessions
                if s.instrument_id in ids and request.start <= s.session_date <= request.end
            )
        ),
        tuple(
            (
                b
                for b in data.bars
                if b.instrument_id in ids and request.start <= b.session_date <= request.end
            )
        ),
        tuple(
            (
                a
                for a in data.actions
                if a.instrument_id in ids and request.start <= a.effective_at.date() <= request.end
            )
        ),
        tuple(
            (
                q
                for q in data.fx
                if q.currency in {i.currency for i in data.instruments if i.instrument_id in ids}
                and q.observed_at.date() <= request.end
            )
        ),
        data.provenance,
    )


def known_at(data: MarketData, at: datetime) -> MarketData:
    return MarketData(
        data.instruments,
        tuple((s for s in data.sessions if s.close_at <= at)),
        tuple((b for b in data.bars if b.available_at <= at and b.close_at <= at)),
        tuple((a for a in data.actions if a.available_at <= at and a.effective_at <= at)),
        tuple((q for q in data.fx if q.available_at <= at and q.observed_at <= at)),
        data.provenance,
    )
