"""Tests for :mod:`bascom.cli`."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from bascom import debug_option
import click

if TYPE_CHECKING:
    from click.testing import CliRunner
    from pytest_mock import MockerFixture


def test_debug_option_adds_flag_and_calls_setup(mocker: MockerFixture, runner: CliRunner) -> None:
    setup = mocker.patch('bascom.cli.setup_logging')

    @click.command()
    @debug_option({'myproject': {}})
    def cmd() -> None:
        click.echo('ran')

    result = runner.invoke(cmd, ['--debug'])
    assert result.exit_code == 0
    assert 'ran' in result.output
    setup.assert_called_once_with(debug=True, loggers={'myproject': {}})


def test_debug_option_defaults_to_no_debug(mocker: MockerFixture, runner: CliRunner) -> None:
    setup = mocker.patch('bascom.cli.setup_logging')

    @click.command()
    @debug_option()
    def cmd() -> None:
        pass

    assert runner.invoke(cmd, []).exit_code == 0
    setup.assert_called_once_with(debug=False, loggers={})


def test_debug_option_preserves_wrapped_options(mocker: MockerFixture, runner: CliRunner) -> None:
    mocker.patch('bascom.cli.setup_logging')

    @click.option('--foo')
    def callback(foo: str | None = None) -> None:
        click.echo(f'foo={foo}')

    before = [p.name for p in cast('Any', callback).__click_params__]
    cmd = click.command()(debug_option()(callback))

    assert [p.name for p in cast('Any', callback).__click_params__] == before
    assert sorted(p.name for p in cmd.params) == ['debug', 'foo']
    result = runner.invoke(cmd, ['--foo', 'bar', '--debug'])
    assert result.exit_code == 0
    assert 'foo=bar' in result.output


def test_debug_option_help_lists_flag(runner: CliRunner) -> None:
    @click.command()
    @debug_option()
    def cmd() -> None:
        pass

    out = runner.invoke(cmd, ['--help']).output
    assert '--debug' in out


def test_debug_option_copies_loggers(mocker: MockerFixture, runner: CliRunner) -> None:
    setup = mocker.patch('bascom.cli.setup_logging')
    loggers: dict[str, Any] = {'myproject': {}}
    decorator = debug_option(loggers)
    loggers['other'] = {}

    @click.command()
    @decorator
    def cmd() -> None:
        pass

    assert runner.invoke(cmd, []).exit_code == 0
    setup.assert_called_once_with(debug=False, loggers={'myproject': {}})


def test_debug_option_returns_callback_value(mocker: MockerFixture, runner: CliRunner) -> None:
    mocker.patch('bascom.cli.setup_logging')

    @click.command()
    @debug_option()
    def cmd() -> str:
        return 'value'

    result = runner.invoke(cmd, [], standalone_mode=False)
    assert result.exit_code == 0
    assert result.return_value == 'value'
