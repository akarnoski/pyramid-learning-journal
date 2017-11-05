"""Pytest fixtures for testing."""
from pyramid import testing
import pytest


@pytest.fixture
def dummy_request():
    return testing.DummyRequest()
