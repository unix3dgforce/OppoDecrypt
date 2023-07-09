__author__ = "MiuiPro.info DEV Team"
__copyright__ = "Copyright (c) 2023 MiuiPro.info"

__all__ = ["ValidationError"]


class ValidationError(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)
        self.message = message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message{self.message})"
