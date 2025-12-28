"""Utilities."""
from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypedDict
import logging
import logging.config
import os

from colorlog import default_log_colors
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

__all__ = ('LogColors', 'SetupLoggingKwargs', 'setup_logging')

_DEBUG_NO_TIME_FORMAT = ('%(log_color)s%(levelname)-8s%(reset)s | '
                         '%(light_green)s%(name)s%(reset)s:%(light_red)s%(funcName)s%(reset)s:'
                         '%(blue)s%(lineno)d%(reset)s - %(message)s')
_DEFAULT_LOG_COLORS = default_log_colors | {'INFO': 'light_white', 'CRITICAL': 'bold_light_red'}


class LogColors(TypedDict, total=False):
    """A dictionary of log colors."""

    CRITICAL: str
    """Colour for CRITICAL log level."""
    DEBUG: str
    """Colour for DEBUG log level."""
    ERROR: str
    """Colour for ERROR log level."""
    INFO: str
    """Colour for INFO log level."""
    WARNING: str
    """Colour for WARNING log level."""


class SetupLoggingKwargs(TypedDict, total=False):
    """Keyword arguments for :py:func:`.setup_logging`."""
    formatters: dict[str, _FormatterConfiguration]
    """Formatters to add to the logging configuration."""
    filters: dict[str, _FilterConfiguration]
    """Filters to add to the logging configuration."""
    handlers: dict[str, _HandlerConfiguration]
    """Handlers to add to the logging configuration."""
    incremental: bool
    """If ``True``, the configuration is merged with the existing configuration."""
    loggers: dict[str, _LoggerConfiguration]
    """Loggers to add to the logging configuration."""
    root: _RootLoggerConfiguration
    """Root logger configuration."""


def setup_logging(*,
                  debug: bool = False,
                  disable_existing_loggers: bool = True,
                  force_color: bool = False,
                  no_color: bool = False,
                  formatter: Literal['debug', 'debug-no-time', 'default'] | None = None,
                  log_colors: LogColors | None = None,
                  **kwargs: Unpack[SetupLoggingKwargs]) -> None:
    """
    Set up logging configuration.

    Most of the time, the following is sufficient::

        from bascom import setup_logging
        setup_logging(debug=debug_param, loggers={'your_logger_name': {}})

    This calls :py:func:`logging.config.dictConfig` with a configuration that logs to the console
    with `colorlog <https://pypi.org/project/colorlog/>`_'s
    :py:class:`colorlog.formatter.ColoredFormatter`. It adds a single handler ``console`` to the
    root logger.

    By default, the formatter for the console handler is set to ``debug`` if ``debug`` is ``True``,
    otherwise to ``default``. The ``debug`` formatter includes timestamps and more detailed
    information, while the ``default`` formatter only logs the message. The formatter can be
    overridden by setting the environment variable ``BASCOM_CONSOLE_FORMATTER`` to either
    ``debug``, ``debug-no-time``, or ``default``.

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
    formatter : Literal['debug', 'debug-no-time', 'default']
        Formatter to use for the console handler.
    log_colors : LogColors | None
        Log colors to use for the ``ColoredFormatter``. Specifying every colour is not required as
        the defaults will be merged.
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
                'format': '%(log_color)s%(message)s',
                'log_colors': _DEFAULT_LOG_COLORS | (log_colors or {}),
                'no_color': no_color,
            },
            'debug-no-time': {
                '()': 'colorlog.ColoredFormatter',
                'force_color': force_color,
                'format': _DEBUG_NO_TIME_FORMAT,
                'log_colors': _DEFAULT_LOG_COLORS | (log_colors or {}),
                'no_color': no_color,
            },
            'debug': {
                '()': 'colorlog.ColoredFormatter',
                'force_color': force_color,
                'format': f'%(light_cyan)s%(asctime)s%(reset)s | {_DEBUG_NO_TIME_FORMAT}',
                'log_colors': _DEFAULT_LOG_COLORS | (log_colors or {}),
                'no_color': no_color,
            }
        } | formatters,
        'handlers': {
            'console': {
                'class':
                    'colorlog.StreamHandler',
                'formatter':
                    os.environ.get('BASCOM_CONSOLE_FORMATTER', formatter or
                                   ('debug' if debug else 'default')),
            }
        } | handlers,
        'root': {
            'level': 'DEBUG' if debug else 'INFO',
            'handlers': ('console',)
        } | root,
        'version': 1
    } | kwargs)
