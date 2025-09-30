"""Utilities."""
from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict
import logging
import logging.config

from typing_extensions import Unpack

log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from logging.config import (
        _FilterConfiguration,
        _FormatterConfiguration,
        _HandlerConfiguration,
        _LoggerConfiguration,
        _RootLoggerConfiguration,
    )


class SetupLoggingKwargs(TypedDict, total=False):
    """Keyword arguments for :py:func:`setup_logging`."""
    formatters: dict[str, _FormatterConfiguration]
    filters: dict[str, _FilterConfiguration]
    handlers: dict[str, _HandlerConfiguration]
    incremental: bool
    loggers: dict[str, _LoggerConfiguration]
    root: _RootLoggerConfiguration


def setup_logging(*,
                  debug: bool = False,
                  disable_existing_loggers: bool = True,
                  force_color: bool = False,
                  no_color: bool = False,
                  **kwargs: Unpack[SetupLoggingKwargs]) -> None:
    """
    Set up logging configuration.

    This calls :py:func:`logging.config.dictConfig` with a configuration that logs to the console
    with `colorlog <https://pypi.org/project/colorlog/>`_'s
    :py:class:`colorlog.formatter.ColoredFormatter`. It adds a single handler ``console`` to the
    root logger.

    All keyword arguments are merged into the configuration dictionary passed to
    :py:func:`logging.config.dictConfig`. The keys ``root``, ``formatters``, and ``handlers``
    are popped from the keyword arguments and merged into the respective sections of the
    configuration.

    See `NO_COLOR <https://no-color.org/>`_.

    Parameters
    ----------
    debug : bool
        If ``True``, set the log level to ``DEBUG``. Otherwise, set it to ``INFO``.
    disable_existing_loggers : bool
        If ``True``, disable any existing loggers when configuring logging.
    force_color : bool
        If ``True``, force color output even if the output is not a TTY. This will override
        the ``NO_COLOR`` environment variable and takes precedence over the ``no_color`` parameter.
    no_color : bool
        If ``True``, disable color output. This can be overriden with environment variable
        ``NO_COLOR``.
    """
    root = kwargs.pop('root', {})
    formatters = kwargs.pop('formatters', {})
    handlers = kwargs.pop('handlers', {})
    logging.config.dictConfig({
        'disable_existing_loggers': disable_existing_loggers,
        'formatters': {
            'default': {
                '()': 'colorlog.ColoredFormatter',
                'force_color': force_color,
                'format':
                    ('%(light_cyan)s%(asctime)s%(reset)s | %(log_color)s%(levelname)-8s%(reset)s | '
                     '%(light_green)s%(name)s%(reset)s:%(light_red)s%(funcName)s%(reset)s:'
                     '%(blue)s%(lineno)d%(reset)s - %(message)s'),
                'no_color': no_color,
            }
        } | formatters,
        'handlers': {
            'console': {
                'class': 'colorlog.StreamHandler',
                'formatter': 'default',
            }
        } | handlers,
        'root': {
            'level': 'DEBUG' if debug else 'INFO',
            'handlers': ('console',)
        } | root,
        'version': 1
    } | kwargs)
