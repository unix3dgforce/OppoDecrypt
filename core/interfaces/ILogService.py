import abc
from typing import Callable

from core.models import LogLevel

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'


class ILogService(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def get_current_logger(self):
        """Get Logger"""

    @classmethod
    @abc.abstractmethod
    def add_logger_sink(cls, func: Callable, **kwargs):
        """Add logger sink"""

    @classmethod
    @abc.abstractmethod
    def log(cls, level: LogLevel, message: str, exception: Exception = None):
        """Add to log"""

    @classmethod
    def critical(cls, message: str, exception: Exception = None):
        cls.log(LogLevel.Critical, message, exception)

    @classmethod
    def debug(cls, message: str, exception: Exception = None):
        cls.log(LogLevel.Debug, message, exception)

    @classmethod
    def error(cls, message: str, exception: Exception = None):
        cls.log(LogLevel.Error, message, exception)

    @classmethod
    def information(cls, message: str):
        cls.log(LogLevel.Info, message)

    @classmethod
    def trace(cls, message: str):
        cls.log(LogLevel.Trace, message)

    @classmethod
    def warning(cls, message: str):
        cls.log(LogLevel.Warning, message)
