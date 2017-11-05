from pyramid_learning_journal.data.journal_entries import JOURNAL_ENTRIES
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPBadRequest
from pyramid import testing
import pytest


def test_list_view_returns_dict(dummy_request):
    """List view returns a Response object."""
    from pyramid_learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert isinstance(response, dict)


def test_list_view_returns_proper_amount_of_content(dummy_request):
    """List view response has corrent content amount."""
    from pyramid_learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert len(response['entry']) == len(JOURNAL_ENTRIES)


def test_detail_view_returns_dict(dummy_request):
    """Test that detail view returns a dictionary of values."""
    from pyramid_learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 1
    response = detail_view(dummy_request)
    assert isinstance(response, dict)


def test_detail_view_raises_error(dummy_request):
    """Test that detail view raises error when id is not found."""
    from pyramid_learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 100
    with pytest.raises(HTTPNotFound):
        response = detail_view(dummy_request)


def test_detail_view_dict_is_not_empty(dummy_request):
    """Detail view returns dictionary that is not empty."""
    from pyramid_learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 1
    response = detail_view(dummy_request)
    assert any(response) is True


def test_detail_view_returns_all_dict_attr(dummy_request):
    """Detail view returns all keys in the object."""
    from pyramid_learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 1
    response = detail_view(dummy_request)
    for key in ["id", "title", "date", "body"]:
        assert key in response['post'].keys()


def test_create_view_returns_dict(dummy_request):
    """Create view returns a dictionary."""
    from pyramid_learning_journal.views.default import create_view
    response = create_view(dummy_request)
    assert isinstance(response, dict)


def test_create_view_returns_empty_dict(dummy_request):
    """Create view dictionary is empty."""
    from pyramid_learning_journal.views.default import create_view
    response = create_view(dummy_request)
    assert any(response) is False


def test_update_view_returns_dict(dummy_request):
    """Test that detail view returns a dictionary of values."""
    from pyramid_learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 1
    response = update_view(dummy_request)
    assert isinstance(response, dict)


def test_update_view_dict_is_not_empty(dummy_request):
    """Update view returns dictionary that is not empty."""
    from pyramid_learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 1
    response = update_view(dummy_request)
    assert any(response) is True


def test_update_view_returns_all_dict_attr(dummy_request):
    """Update view returns all keys in the object."""
    from pyramid_learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 1
    response = update_view(dummy_request)
    for key in ["id", "title", "date", "body"]:
        assert key in response['post'].keys()


def test_update_view_raises_error(dummy_request):
    """Test that update view raises error when id is not found."""
    from pyramid_learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 100
    with pytest.raises(HTTPNotFound):
        response = update_view(dummy_request)
