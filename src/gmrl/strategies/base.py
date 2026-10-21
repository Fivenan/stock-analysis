from datetime import datetime
from typing import Protocol

from gmrl.domain import MarketData, TargetWeights


class Strategy(Protocol):
    def weights(self, history: MarketData, decided_at: datetime) -> TargetWeights: ...
