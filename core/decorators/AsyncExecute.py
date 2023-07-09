import asyncio
from functools import wraps, partial

__author__ = "MiuiPro.info DEV Team"
__copyright__ = "Copyright (c) 2023 MiuiPro.info"


class AsyncExecute:
    def __new__(cls, decorated_func=None, **kwargs):
        self = super().__new__(cls)

        return self.__call__(decorated_func) if decorated_func else self

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            loop = asyncio.get_running_loop()
            pfunc = partial(func, *args, **kwargs)
            return await loop.run_in_executor(None, pfunc)
        return wrapper
