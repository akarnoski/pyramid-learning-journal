import pytest
from pyramid import testing
import transaction
from pyramid_learning_journal.models import (
    Entry,
    get_tm_session,
)
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPBadRequest
from pyramid_learning_journal.models.meta import Base
from faker import Faker


def test_list_view_returns_empty_when_database_empty(dummy_request):
    """List view returns nothing when there is no data."""
    from pyramid_learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert len(response['entries']) == 0


def test_list_view_returns_count_matching_database(dummy_request, add_models):
    """Home view response matches database count."""
    from pyramid_learning_journal.views.default import list_view
    response = list_view(dummy_request)
    query = dummy_request.dbsession.query(Entry)
    assert len(response['entries']) == query.count()


def test_list_view_returns_dict(dummy_request):
    """List view returns a Response object."""
    from pyramid_learning_journal.views.default import list_view
    response = list_view(dummy_request)
    query = dummy_request.dbsession.query(Entry).all()
    assert isinstance(response, dict)


def test_create_view_post_empty_is_empty_dict(dummy_request):
    """POST requests without data should return an empty dictionary."""
    from pyramid_learning_journal.views.default import create_view
    dummy_request.method = "POST"
    response = create_view(dummy_request)
    assert response == {}


def test_create_view_post_incomplete_data_returns_data(dummy_request):
    """POST data that is incomplete just gets returned to the user."""
    from pyramid_learning_journal.views.default import create_view
    dummy_request.method = "POST"
    data_dict = {"title": 'this is a test'}
    dummy_request.POST = data_dict
    response = create_view(dummy_request)
    assert response == data_dict


def test_create_view_post_good_data_is_302(dummy_request):
    """POST request with correct data should redirect with status code 302."""
    from pyramid_learning_journal.views.default import create_view
    dummy_request.method = "POST"
    data_dict = {
            "title": "testing title",
            "date": "10 Fake, Year",
            "tags": "yes, no, okay",
            "body": "I hope this works"
    }
    dummy_request.POST = data_dict
    response = create_view(dummy_request)
    assert response.status_code == 302


def test_detail_view_raises_error(dummy_request):
    """Test that detail view raises error when id is not found."""
    from pyramid_learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 100
    with pytest.raises(HTTPNotFound):
        response = detail_view(dummy_request)
