from typing import Protocol
from gmrl.domain import Instrument, DatasetRequest, MarketData, ProviderStatus


class DataProvider(Protocol):
    def instruments(self) -> tuple[Instrument, ...]: ...

    def fetch(self, request: DatasetRequest) -> MarketData: ...

    def status(self) -> ProviderStatus: ...
