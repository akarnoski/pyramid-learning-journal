import unittest
import transaction

from pyramid import testing
from pyramid.response import Response


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


def test_list_view_returns_response():
    """List view returns a Response object."""
    from pyramid_learning_journal.views.default import list_view
    request = testing.DummyRequest()
    response = list_view(request)
    assert isinstance(response, Response)


def test_detail_view_returns_response():
    """Detail view returns a Response object."""
    from pyramid_learning_journal.views.default import detail_view
    request = testing.DummyRequest()
    response = detail_view(request)
    assert isinstance(response, Response)


def test_create_view_returns_response():
    """Create view returns a Response object."""
    from pyramid_learning_journal.views.default import create_view
    request = testing.DummyRequest()
    response = create_view(request)
    assert isinstance(response, Response)


def test_update_view_returns_response():
    """Update view returns a Response object."""
    from pyramid_learning_journal.views.default import update_view
    request = testing.DummyRequest()
    response = update_view(request)
    assert isinstance(response, Response)


def test_list_view_is_good():
    """List view response has a status 200 OK."""
    from pyramid_learning_journal.views.default import list_view
    request = testing.DummyRequest()
    response = list_view(request)
    assert response.status_code == 200


def test_detail_view_is_good():
    """Detail view response has a status 200 OK."""
    from pyramid_learning_journal.views.default import detail_view
    request = testing.DummyRequest()
    response = detail_view(request)
    assert response.status_code == 200


def test_create_view_is_good():
    """Create view response has a status 200 OK."""
    from pyramid_learning_journal.views.default import create_view
    request = testing.DummyRequest()
    response = create_view(request)
    assert response.status_code == 200


def test_update_view_is_good():
    """Update view response has a status 200 OK."""
    from pyramid_learning_journal.views.default import update_view
    request = testing.DummyRequest()
    response = update_view(request)
    assert response.status_code == 200
