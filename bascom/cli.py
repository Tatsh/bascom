"""Click helpers."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast
import functools

import click

from .utils import setup_logging

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping
    from logging.config import _LoggerConfiguration

__all__ = ('debug_option',)


def debug_option(
    loggers: Mapping[str, _LoggerConfiguration] | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Make a ``-d/--debug`` decorator that routes a Click command through :py:func:`.setup_logging`.

    This is a decorator *factory*: call it with the loggers to enable, then apply the result to a
    Click command. The wrapper consumes the ``debug`` flag and does not forward it, so the wrapped
    callback does not need to declare it::

        from bascom import debug_option

        debug = debug_option({'myproject': {}})

        @click.command()
        @debug
        def cmd() -> None:
            ...

    Any Click parameters already applied to the callback are copied onto the wrapper instead of
    being shared with it, so decorating a function never mutates the caller's own function.

    Parameters
    ----------
    loggers : Mapping[str, _LoggerConfiguration] | None
        Loggers to switch to ``DEBUG`` when ``-d/--debug`` is passed. The mapping is copied when
        this function is called, so later changes to it have no effect. If ``None``, no per-logger
        configuration is added.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        A decorator that adds the ``-d/--debug`` flag to a Click command callback.
    """
    config = dict(loggers or {})

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, debug: bool = False, **kwargs: Any) -> Any:
            setup_logging(debug=debug, loggers=config)
            return func(*args, **kwargs)

        # ``functools.wraps`` copies ``__dict__`` entries by reference, so the Click parameter
        # list would be shared with the wrapped callback, and appending to it would mutate the
        # caller's own function. Click stores parameters on an undocumented attribute, hence the
        # cast.
        cast('Any', wrapper).__click_params__ = list(getattr(func, '__click_params__', []))
        return click.option('-d', '--debug', is_flag=True,
                            help='Enable debug level logging.')(wrapper)

    return decorator
