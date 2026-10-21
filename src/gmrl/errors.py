class GMRLError(Exception):
    """Base for actionable laboratory errors."""


class DataValidationError(GMRLError):
    pass


class DataUnavailableError(GMRLError):
    pass


class QuotaExceededError(GMRLError):
    pass


class OrderRejectedError(GMRLError):
    pass


class AccountingError(GMRLError):
    pass


class AuthenticationError(GMRLError):
    pass


class TransientProviderError(DataUnavailableError):
    def __init__(self, message: str, retry_after: float = 0):
        super().__init__(message)
        self.retry_after = retry_after
