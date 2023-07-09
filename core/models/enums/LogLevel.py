from enum import Flag

__author__ = 'MiuiPro.info DEV Team'
__copyright__ = 'Copyright (c) 2023 MiuiPro.info'


class LogLevel(Flag):
    Trace = 5
    Debug = 10
    Info = 20
    Warning = 30
    Error = 40
    Critical = 50

    def __str__(self):
        return self.value
