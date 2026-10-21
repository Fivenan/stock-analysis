from decimal import Decimal
from pathlib import Path
import os
from pydantic import BaseModel, ConfigDict, Field


class Settings(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    runtime: Path = Path(".runtime")
    offline: bool = True
    cache_ttl_seconds: int = Field(default=3600, ge=0)
    initial_cash_eur: Decimal = Field(default=Decimal("10000"), gt=0, allow_inf_nan=False)


def load_settings() -> Settings:
    raw = os.environ.get("GMRL_OFFLINE", "true").lower()
    if raw not in ("true", "false"):
        raise ValueError("GMRL_OFFLINE must be true or false")
    return Settings(runtime=Path(os.environ.get("GMRL_RUNTIME", ".runtime")), offline=raw == "true")
