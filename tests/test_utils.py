from __future__ import annotations

from typing import TYPE_CHECKING

from bascom import setup_logging

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


def test_setup_logging(mocker: MockerFixture) -> None:
    mock_dc = mocker.patch('logging.config.dictConfig')
    setup_logging(debug=True, force_color=True, handlers={'custom': {'class': 'MyHandler'}})
    mock_dc.assert_called_once_with({
        'disable_existing_loggers': True,
        'formatters': {
            'default': {
                '()': 'colorlog.ColoredFormatter',
                'force_color': True,
                'format': '%(log_color)s%(message)s',
                'log_colors': {
                    'DEBUG': 'white',
                    'INFO': 'light_white',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_light_red'
                },
                'no_color': False
            },
            'debug-no-time': {
                '()': 'colorlog.ColoredFormatter',
                'force_color': True,
                'format': ('%(log_color)s%(levelname)-8s%(reset)s | '
                           '%(light_green)s%(name)s%(reset)s:%(light_red)s%(funcName)s%(reset)s:'
                           '%(blue)s%(lineno)d%(reset)s - %(message)s'),
                'log_colors': {
                    'DEBUG': 'white',
                    'INFO': 'light_white',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_light_red'
                },
                'no_color': False
            },
            'debug': {
                '()': 'colorlog.ColoredFormatter',
                'force_color': True,
                'format': (
                    '%(light_cyan)s%(asctime)s%(reset)s | '
                    '%(log_color)s%(levelname)-8s%(reset)s | %(light_green)s%(name)s%(reset)s:'
                    '%(light_red)s%(funcName)s%(reset)s:%(blue)s%(lineno)d%(reset)s - %(message)s'),
                'log_colors': {
                    'DEBUG': 'white',
                    'INFO': 'light_white',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_light_red'
                },
                'no_color': False
            }
        },
        'handlers': {
            'console': {
                'class': 'colorlog.StreamHandler',
                'formatter': 'debug'
            },
            'custom': {
                'class': 'MyHandler'
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ('console',)
        },
        'version': 1
    })
