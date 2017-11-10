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


def test_new_entry_redirects_to_home(testapp, empty_db):
    """When redirection is followed, result is home page."""
    data_dict = {
        "title": "testing title",
        "date": "10 Fake, Year",
        "tags": "yes, no, okay",
        "body": "I hope this works"
    }
    response = testapp.post('/journal/new-entry', data_dict)
    next_response = response.follow()
    home_response = testapp.get('/')
    assert next_response.text == home_response.text


def test_layout_root(testapp, empty_db):
    """Test that the contents of the root page contains blog title."""
    response = testapp.get('/', status=200)
    html = response.html
    assert 'Python Learning Journal' in html.find("h1").text


def test_layout_has_correct_article_count(testapp, fill_the_db):
    """Test that the contents same number of articles as fake entries."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(FAKE_ENTRIES) == len(html.findAll("article"))


def test_detail_page(testapp):
    """Test the detail page opens without error."""
    response = testapp.get('/journal/5', status=200)
    html = response.html
    assert 'Python Learning Journal' in html.find("h1").text


def test_detail_page_error_opens_404_message(testapp, fill_the_db):
    """Test the detail page opens without error."""
    response = testapp.get('/journal/50', status=404)
    html = response.html
    assert '404' in html.find("span").text


def test_detail_page_renders_post_body(testapp, fill_the_db):
    """Test the article body replaced the template expression."""
    response = testapp.get('/journal/7', status=200)
    html = response.html
    assert html.find("p").text != '{{body}}'


def test_edit_page(testapp, fill_the_db):
    """Test create page renders without error."""
    response = testapp.get('/journal/13/edit-entry', status=200)
    html = response.html
    assert html.find("form")


def test_edit_page(testapp, fill_the_db):
    """Test create page renders without error."""
    response = testapp.get('/journal/13/edit-entry', status=200)
    html = response.html
    assert html.find("form")


def test_delete_verification_page(testapp, fill_the_db):
    """Test delete verifiation page renders without error."""
    response = testapp.get('/journal/6/verification', status=200)
    html = response.html
    assert html.find("form")