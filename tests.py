from pyramid import testing
import pytest


@pytest.fixture
def dummy_request():
    return testing.DummyRequest()


def test_list_view_response_status_code(dummy_request):
    """."""
    from pyramid_learning_journal.views.default import list_view
    list_response = list_view(dummy_request)
    assert list_response.status_code == 200
