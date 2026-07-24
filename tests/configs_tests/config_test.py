"""Test battery for the config module."""

import pytest
from typing import Any
from src.enums.config_keys import ConfigKey
from src.utils import Point
import src.utils.config as u


def test_load_confing_example() -> None:
    """Must assert True because all 7 lines in the config.example are valid."""
    assert len(u.load_config("config.example")) == 7


def test_load_config_returns_dict() -> None:
    """Must assert True because the function load_config returns a dict."""
    assert isinstance(u.load_config("config.example"), dict)


def test_load_config_missing_lines() -> None:
    """Must assert True for all files to attest that all are missing keys.

    Should Raise Exception when critical values are missing instead
    """
    conf: dict[ConfigKey, Any] = u.load_config(
        "tests/configs_tests" + "/6lines_config.txt"
    )
    with pytest.raises(AssertionError):
        assert len(conf) == 7
    with pytest.raises(KeyError):
        conf[ConfigKey.SEED]
    conf = u.load_config("tests/configs_tests" + "/5lines_config.txt")
    with pytest.raises(AssertionError):
        assert len(conf) == 7
    with pytest.raises(KeyError):
        conf[ConfigKey.SEED]
    conf = u.load_config("tests/configs_tests" + "/3lines_config.txt")
    with pytest.raises(AssertionError):
        assert len(conf) == 7
    with pytest.raises(KeyError):
        conf[ConfigKey.SEED]


def test_check_invalid_line() -> None:
    """."""
    with pytest.raises(ValueError):
        u._get_config_line("INVALID_KEY=True")


def test_check_valid_width() -> None:
    """."""
    assert u._get_config_line("WIDTH=5") == (ConfigKey.WIDTH, 5)


def test_check_invalid_height() -> None:
    """."""
    with pytest.raises(ValueError):
        assert u._get_config_line("HEIGHT=-5") == (ConfigKey.HEIGHT, -5)


def test_check_valid_entry() -> None:
    """."""
    assert u._get_config_line("ENTRY=0,5") == (ConfigKey.ENTRY, Point(0, 5))


def test_check_invalid_exit() -> None:
    """."""
    with pytest.raises(ValueError):
        assert u._get_config_line("EXIT=-5,-123") == (
            ConfigKey.EXIT,
            Point(-5, -123),
        )


def test_valid_output_file() -> None:
    """."""
    assert u._get_config_line("OUTPUT_FILE=test_maze.txt") == (
        ConfigKey.OUTPUT_FILE,
        "test_maze.txt",
    )


def test_invalid_output_file() -> None:
    """."""
    with pytest.raises(PermissionError):
        assert u._get_config_line("OUTPUT_FILE=/bin/test_maze.txt") == (
            ConfigKey.OUTPUT_FILE,
            "test_maze.txt",
        )


def test_valid_perfect_true() -> None:
    """."""
    assert u._get_config_line("PERFECT=True") == (ConfigKey.PERFECT, True)


def test_valid_perfect_false() -> None:
    """."""
    assert u._get_config_line("PERFECT=False") == (ConfigKey.PERFECT, False)


def test_invalid_perfect_true() -> None:
    """."""
    with pytest.raises(ValueError):
        assert u._get_config_line("PERFECT=Prout") == (ConfigKey.PERFECT, True)


def test_invalid_perfect_false() -> None:
    """."""
    with pytest.raises(ValueError):
        assert u._get_config_line("PERFECT=Prout") == (
            ConfigKey.PERFECT,
            False
        )
