"""Test __init__.py."""
from fastapi import FastAPI

from intape import app


def test_app_fabric():
    """Test app fabric."""
    assert isinstance(app(), FastAPI)
