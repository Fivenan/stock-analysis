import csv
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from gmrl.domain import Bar, Instrument, Provenance, MarketData, Session
from gmrl.data.validation import validate_market_data
from gmrl.errors import DataValidationError


def _parse_bar(row: dict[str, str], provenance_id: str) -> Bar:
    if row["price_basis"] != "raw":
        raise DataValidationError("CSV price_basis must explicitly equal raw")
    return Bar(
        instrument_id=row["instrument_id"],
        session_date=date.fromisoformat(row["session_date"]),
        open_at=datetime.fromisoformat(row["open_at"]),
        close_at=datetime.fromisoformat(row["close_at"]),
        available_at=datetime.fromisoformat(row["available_at"]),
        open=Decimal(row["open"]),
        high=Decimal(row["high"]),
        low=Decimal(row["low"]),
        close=Decimal(row["close"]),
        volume=Decimal(row["volume"]),
        price_basis="raw",
        provenance_id=provenance_id,
    )


def import_bars_csv(
    path: Path, instruments: tuple[Instrument, ...], provenance: Provenance
) -> tuple[Bar, ...]:
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = tuple(
                _parse_bar(row, provenance.provenance_id) for row in csv.DictReader(handle)
            )
        sessions = tuple(
            Session(b.instrument_id, b.session_date, b.open_at, b.close_at) for b in rows
        )
        validate_market_data(MarketData(instruments, sessions, rows, (), (), (provenance,)))
        return rows
    except (KeyError, ValueError, InvalidOperation) as exc:
        raise DataValidationError("Invalid CSV columns, ISO timestamps or decimal values") from exc
