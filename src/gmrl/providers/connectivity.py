"""Optional read-only public connectivity; never called by offline providers.
No authentication, account, quote feed, securities access or rights claim.
"""

import json
from urllib.request import Request, urlopen
from urllib.error import URLError
from gmrl.errors import DataUnavailableError, DataValidationError

ENDPOINTS = {
    "worldbank": "https://api.worldbank.org/v2/country/DEU/indicator/NY.GDP.MKTP.CD?date=2023&format=json"
}


def test_connection(provider: str, *, timeout: float = 5.0, transport=None) -> dict[str, object]:
    if provider not in ENDPOINTS:
        raise DataValidationError("Public connectivity probe not configured")
    if timeout <= 0 or timeout > 30:
        raise DataValidationError("Timeout must be in (0,30]")
    url = ENDPOINTS[provider]
    try:
        opener = transport or urlopen
        with opener(
            Request(url, headers={"User-Agent": "GMRL-read-only-connectivity/0.1"}), timeout=timeout
        ) as response:
            payload = response.read(1000001)
            if len(payload) > 1000000:
                raise DataUnavailableError("Response exceeds probe size bound")
            data = json.loads(payload)
            valid = (
                isinstance(data, list)
                and len(data) == 2
                and isinstance(data[0], dict)
                and isinstance(data[1], list)
                and any(
                    (
                        row.get("countryiso3code") == "DEU"
                        and row.get("indicator", {}).get("id") == "NY.GDP.MKTP.CD"
                        for row in data[1]
                        if isinstance(row, dict)
                    )
                )
            )
            if not valid:
                raise DataUnavailableError("World Bank GDP schema did not match")
            return {
                "provider": provider,
                "source": url,
                "http_status": response.status,
                "schema_valid": True,
                "scope": "Public annual GDP metadata connectivity only; no live market quotes",
            }
    except (URLError, OSError, ValueError) as exc:
        raise DataUnavailableError(
            "Public connectivity failed; offline sample remains available"
        ) from exc
