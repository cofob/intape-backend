"""Test config.py."""
from os import environ

import pytest
from faker import Faker

from intape.core.config import Config


def test_config_from_env():
    """Test Config.from_env."""
    assert isinstance(Config.from_env(), Config)


def check_ipfs_auth(username: str, password: str) -> bool:
    """Check IPFS_AUTH."""
    environ["IPFS_AUTH"] = f"{username}:{password}"
    config = Config.from_env()
    return config.IPFS_AUTH == (username, password)


@pytest.mark.parametrize("password", ["{}", ":{}", "{}:", ":{}:", "::::::"])
def test_ipfs_auth(faker: Faker, password: str):
    """Test IPFS_AUTH."""
    username = faker.user_name()
    assert check_ipfs_auth(username, password.format(faker.password()))


def test_origins():
    """Test ORIGINS."""
    environ["ORIGINS"] = "http://localhost:3000,http://localhost:5000"
    config = Config.from_env()
    assert config.ORIGINS == ("http://localhost:3000", "http://localhost:5000")


def test_get_env_error_raise():
    """Test Config._get_env."""
    with pytest.raises(ValueError):
        Config._get_env("NOT_EXISTING_ENV_VAR")


def test_get_env_not_existing():
    """Test Config._get_env."""
    val = Config._get_env("NOT_EXISTING_ENV_VAR", "default")
    assert val == "default"


def test_get_env_existing(faker: Faker):
    """Test Config._get_env."""
    environ[key := faker.word()] = faker.pystr()
    returned = Config._get_env(key)
    assert returned == environ[key]
