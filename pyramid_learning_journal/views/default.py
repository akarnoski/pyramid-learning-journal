"""Render different views based on page selection."""
from pyramid.view import view_config
from pyramid_learning_journal.models.entry import Entry
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound,
    HTTPForbidden)
from pyramid.security import remember, forget
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid_learning_journal.security import check_credentials
import os


@view_config(route_name='home', renderer='../templates/index.jinja2')
def list_view(request):
    """Return all entries in the database."""
    entries = request.dbsession.query(Entry).all()
    entries = sorted(
        [entry.to_dict() for entry in entries],
        key=lambda x: x['id'])
    return {
        "entries": entries
        }


@view_config(route_name='tag_view', renderer='../templates/tag_list.jinja2')
def tag_view(request):
    """Return all entries in the database that have a specific tag."""
    tag = request.matchdict['tag']
    query = request.dbsession.query(Entry).filter(
        Entry.tags.like('%' + tag + '%')).order_by(Entry.id)
    entries = query.all()
    return {
        "entries": entries
        }


@view_config(route_name='detail_page', renderer='../templates/detail.jinja2')
def detail_view(request):
    """Return full entry based on selected id."""
    entry_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entry).get(entry_id)
    if entry:
        return {
            "id": entry.id,
            "title": entry.title,
            "date": entry.date,
            "tags": entry.tags,
            "body": entry.body,
        }
    else:
        raise HTTPNotFound


@view_config(
    route_name='create_article_page',
    renderer='../templates/form_page.jinja2',
    permission='secret')
def create_view(request):
    """Renders new article page and returns user input."""
    if request.method == "GET":
        return {}
    if request.method == "POST" and request.POST:
        form_names = ["title", "date", "tags", "body"]
        if sum([key in request.POST for key in form_names]) == len(form_names):
            if ' ' not in list(request.POST.values()):
                form_data = request.POST
                new_entry = Entry(
                    title=form_data["title"],
                    date=form_data["date"],
                    tags=form_data["tags"],
                    body=form_data["body"],
                )
                request.dbsession.add(new_entry)
                return HTTPFound(request.route_url('home'))
        data = request.POST
        return data
    return {}


@view_config(
    route_name='update_article_page',
    renderer='../templates/edit_page.jinja2',
    permission='secret')
def update_view(request):
    """Renders edit page and updates post using user input."""
    entry_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entry).get(entry_id)
    if not entry:
        raise HTTPNotFound
    if request.method == "GET":
        if entry:
            return {
                "id": entry.id,
                "title": entry.title,
                "date": entry.date,
                "tags": entry.tags,
                "body": entry.body
            }
    if request.method == "POST":
        entry.title = request.POST['title']
        entry.date = request.POST['date']
        entry.tags = request.POST['tags']
        entry.body = request.POST['body']
        request.dbsession.add(entry)
        request.dbsession.flush()
        return HTTPFound(request.route_url('detail_page', id=entry_id))


@view_config(
    route_name='verify_delete',
    renderer='../templates/delete_view.jinja2',
    permission='secret')
def verify_delete(request):
    """Renders delete view using the post id to prepare to delete
    and requests password."""
    entry_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entry).get(entry_id)
    if not entry:
        raise HTTPNotFound
    if request.method == "GET":
        return {
            "id": entry.id,
            "title": entry.title,
            "date": entry.date,
            "tags": entry.tags,
            "body": entry.body,
            }
    if request.method == "POST":
        password = request.POST['password']
        if password == os.environ['PASSWORD']:
            return HTTPFound(request.route_url('delete_entry', id=entry_id))
        else:
            return HTTPFound(request.route_url('verify_delete', id=entry_id))


@view_config(route_name='delete_entry')
def delete_entry(request):
    """Route used to delete post from database."""
    entry_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entry).get(entry_id)
    request.dbsession.delete(entry)
    return HTTPFound(request.route_url('home'))


@view_config(
    route_name='login',
    renderer='../templates/login.jinja2')
def login(request):
    if request.method == 'GET':
        return {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if check_credentials(username, password):
            headers = remember(request, username)
            return HTTPFound(
                location=request.route_url('home'),
                headers=headers)
        request.session.flash('* INCORRECT USERNAME/PASSWORD COMBINATION')
        return {}


@view_config(
    route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)
