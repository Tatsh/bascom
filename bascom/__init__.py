"""bascom module."""
from __future__ import annotations

from .cli import debug_option
from .utils import setup_logging

__all__ = ('debug_option', 'setup_logging')
__version__ = '0.1.3'
