from pyramid.view import view_config
from pyramid_learning_journal.data.journal_entries import JOURNAL_ENTRIES
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPBadRequest


@view_config(route_name='home', renderer='../templates/index.jinja2')
def list_view(request):
    """Renders the list view."""
    return {
        "entry": JOURNAL_ENTRIES
    }


@view_config(
    route_name='detail_page',
    renderer='../templates/detail.jinja2')
def detail_view(request):
    """Renders the detail page."""
    post_id = int(request.matchdict['id'])
    if post_id < 0 or post_id > len(JOURNAL_ENTRIES) - 1:
        raise HTTPNotFound
    post = list(filter(
        lambda post: post['id'] == post_id,
        JOURNAL_ENTRIES)
    )[0]
    return {
        'post': post
    }


@view_config(
    route_name='create_article_page',
    renderer='../templates/form_page.jinja2')
def create_view(request):
    """Renders the create page."""
    return {}


@view_config(
    route_name='update_article_page',
    renderer='../templates/edit_page.jinja2')
def update_view(request):
    """Renders the update page."""
    post_id = int(request.matchdict['id'])
    if post_id < 0 or post_id > len(JOURNAL_ENTRIES) - 1:
        raise HTTPNotFound
    post = list(filter(
        lambda post: post['id'] == post_id,
        JOURNAL_ENTRIES)
    )[0]
    return {
        'post': post
    }
