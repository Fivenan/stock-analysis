from dataclasses import replace
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from gmrl.data.csv_import import import_bars_csv
from gmrl.data.subset import subset
from gmrl.domain import (
    MarketData,
    Session,
    ProviderStatus,
    Instrument,
    Provenance,
    CorporateAction,
    FXQuote,
    DatasetRequest,
)
from gmrl.data.validation import validate_market_data


class CSVProvider:
    """Explicit registry/provenance and optional validated action/FX companions."""

    def __init__(
        self,
        path: Path,
        instruments: tuple[Instrument, ...],
        provenance: Provenance,
        *,
        actions: tuple[CorporateAction, ...] = (),
        fx: tuple[FXQuote, ...] = (),
    ) -> None:
        path = Path(path)
        provenance = replace(
            provenance,
            source="local CSV: " + path.name,
            retrieved_at=datetime.now(timezone.utc),
            content_sha256=sha256(path.read_bytes()).hexdigest(),
        )
        bars = import_bars_csv(path, instruments, provenance)
        self.data = MarketData(
            instruments,
            tuple((Session(b.instrument_id, b.session_date, b.open_at, b.close_at) for b in bars)),
            bars,
            actions,
            fx,
            (provenance,),
        )
        validate_market_data(self.data)

    def instruments(self) -> tuple[Instrument, ...]:
        return self.data.instruments

    def fetch(self, request: DatasetRequest) -> MarketData:
        return subset(self.data, request)

    def status(self) -> ProviderStatus:
        return ProviderStatus(
            "csv", True, "Local validated raw CSV; FX required for non-EUR execution", 0, None
        )
