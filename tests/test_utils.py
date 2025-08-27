from __future__ import annotations

from typing import TYPE_CHECKING

from bascom import setup_logging

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


def test_setup_logging(mocker: MockerFixture) -> None:
    mock_dc = mocker.patch('logging.config.dictConfig')
    setup_logging(debug=True,
                  force_color=True,
                  handlers={'custom': {
                      'class': 'MyHandler'
                  }},
                  arbitrary_key='value')
    mock_dc.assert_called_once_with({
        'disable_existing_loggers': True,
        'root': {
            'level': 'DEBUG',
            'handlers': ('console',)
        },
        'formatters': {
            'default': {
                '()': 'colorlog.ColoredFormatter',
                'force_color': True,
                'format': (
                    '%(light_cyan)s%(asctime)s%(reset)s | %(log_color)s%(levelname)-8s%(reset)s | '
                    '%(light_green)s%(name)s%(reset)s:%(light_red)s%(funcName)s%(reset)s:'
                    '%(blue)s%(lineno)d%(reset)s - %(message)s'),
                'no_color': False,
            }
        },
        'handlers': {
            'console': {
                'class': 'colorlog.StreamHandler',
                'formatter': 'default',
            },
            'custom': {
                'class': 'MyHandler',
            }
        },
        'version': 1,
        'arbitrary_key': 'value'
    })
