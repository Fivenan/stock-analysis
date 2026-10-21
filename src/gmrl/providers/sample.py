"""SYNTHETIC SAMPLE. Arithmetic educational prices, never market observations.
Calendar: weekdays excluding Jan 1 and Dec 25, local 09:00-16:00 in IANA zones.
2024-2025 only. This deliberately simplified calendar is not an exchange calendar.
"""

from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal as D
from hashlib import sha256
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from gmrl.domain import (
    Instrument,
    Session,
    Bar,
    CorporateAction,
    FXQuote,
    Provenance,
    MarketData,
    ProviderStatus,
    DatasetRequest,
)
from gmrl.errors import DataUnavailableError
from gmrl.data.validation import validate_market_data
from gmrl.data.subset import subset

REGIONS = (
    ("US", "USD", "America/New_York", "Technology"),
    ("DE", "EUR", "Europe/Berlin", "Industrials"),
    ("GB", "GBP", "Europe/London", "Financials"),
    ("JP", "JPY", "Asia/Tokyo", "Industrials"),
    ("TW", "TWD", "Asia/Taipei", "Technology"),
    ("KR", "KRW", "Asia/Seoul", "Technology"),
    ("ID", "IDR", "Asia/Jakarta", "Materials"),
    ("CN", "CNY", "Asia/Shanghai", "Consumer"),
    ("HK", "HKD", "Asia/Hong_Kong", "Financials"),
)


def load_demo() -> MarketData:
    instruments = []
    sessions = []
    bars = []
    actions = []
    quotes = []
    provenance_id = "SYNTHETIC-v1"
    rates = ("0.92", "1", "1.17", "0.0062", "0.029", "0.00069", "0.000059", "0.128", "0.118")
    for n, (country, currency, zone, sector) in enumerate(REGIONS):
        try:
            tz = ZoneInfo(zone)
        except ZoneInfoNotFoundError as exc:
            raise DataUnavailableError(
                "IANA timezone database missing: install approved locked tzdata dependency"
            ) from exc
        ident = "DEMO-" + country
        instruments.append(
            Instrument(
                ident,
                "SYNTHETIC SAMPLE " + country,
                None,
                "DEMO",
                currency,
                zone,
                country,
                "equity",
                sector,
                (("sample", ident),),
                date(2024, 1, 1),
                None,
            )
        )
        day = date(2024, 1, 1)
        index = 0
        while day <= date(2025, 12, 31):
            if day.weekday() < 5 and (day.month, day.day) not in ((1, 1), (12, 25)):
                op = datetime.combine(day, time(9), tz).astimezone(timezone.utc)
                cl = datetime.combine(day, time(16), tz).astimezone(timezone.utc)
                sessions.append(Session(ident, day, op, cl))
                price = (
                    D(70 + n * 9) + D(index) * D("0.035") + D(index * (n + 3) % 31 - 15) * D("0.12")
                )
                if n == 0 and day >= date(2025, 6, 2):
                    price /= 2
                close = price + D(index % 7 - 3) * D("0.03")
                if n == 1 and day >= date(2025, 7, 1):
                    price -= 1
                    close -= 1
                bars.append(
                    Bar(
                        ident,
                        day,
                        op,
                        cl,
                        cl + timedelta(minutes=5),
                        price,
                        max(price, close) + D("0.4"),
                        min(price, close) - D("0.4"),
                        close,
                        D(100000 + n * 1000 + index * 17),
                        "raw",
                        provenance_id,
                    )
                )
                observed = datetime.combine(day, time(0), timezone.utc)
                rate = (
                    D(rates[n])
                    if currency == "EUR"
                    else D(rates[n]) * (1 + D(index % 21 - 10) / D(1000))
                )
                quotes.append(FXQuote(currency, observed, observed, rate, provenance_id))
                index += 1
            day += timedelta(days=1)
        if n in (0, 1):
            day = date(2025, 6, 2) if n == 0 else date(2025, 7, 1)
            at = datetime.combine(day, time(8), tz).astimezone(timezone.utc)
            actions.append(
                CorporateAction(
                    "SYNTHETIC-ACTION-" + country,
                    ident,
                    "split" if n == 0 else "dividend",
                    at,
                    at - timedelta(days=7),
                    D(2 if n == 0 else 1),
                    None if n == 0 else at + timedelta(days=14),
                )
            )
    from gmrl.storage.codec import dumps

    digest = sha256(
        dumps(
            (tuple(instruments), tuple(sessions), tuple(bars), tuple(actions), tuple(quotes))
        ).encode()
    ).hexdigest()
    provenance = Provenance(
        provenance_id,
        "sample",
        "deterministic arithmetic generator v1",
        datetime(2026, 1, 1, tzinfo=timezone.utc),
        "Synthetic educational fixture; CC0",
        True,
        digest,
    )
    data = MarketData(
        tuple(instruments),
        tuple(sessions),
        tuple(bars),
        tuple(actions),
        tuple(quotes),
        (provenance,),
    )
    validate_market_data(data)
    return data


class SampleProvider:
    def __init__(self) -> None:
        self._data = load_demo()

    def instruments(self) -> tuple[Instrument, ...]:
        return self._data.instruments

    def fetch(self, request: DatasetRequest) -> MarketData:
        return subset(self._data, request)

    def status(self) -> ProviderStatus:
        return ProviderStatus("sample", True, "Offline SYNTHETIC SAMPLE; no network", 0, None)
