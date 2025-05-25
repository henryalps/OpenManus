import logging
import functools
from typing import Any, Callable, Type, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


def log_io(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return wrapper


class LoggedToolMixin:
    def _run(self, *args: Any, **kwargs: Any) -> Any:
        return super()._run(*args, **kwargs)


def create_logged_tool(base_tool_class: Type[T]) -> Type[T]:
    class LoggedTool(LoggedToolMixin, base_tool_class):
        pass

    return LoggedTool
