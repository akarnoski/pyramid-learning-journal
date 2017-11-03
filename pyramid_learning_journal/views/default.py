"""Render different views based on page selection."""
from pyramid.view import view_config
from pyramid_learning_journal.models.entry import Entry
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPBadRequest


@view_config(route_name='home', renderer='../templates/index.jinja2')
def list_view(request):
    """Return all entries in the database."""
    entries = request.dbsession.query(Entry).all()
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
    renderer='../templates/form_page.jinja2')
def create_view(request):
    """Renders new article page and returns user input."""
    if request.method == "GET":
        return {}
    if request.method == "POST":
        new_entry = Entry(
            title=request.POST["title"],
            date=request.POST["date"],
            tags=request.POST["tags"],
            body=request.POST["body"],
        )
        request.dbsession.add(new_entry)
    return HTTPFound(request.route_url('home'))


@view_config(
    route_name='update_article_page',
    renderer='../templates/edit_page.jinja2')
def update_view(request):
    """Renders edit page and updates post using user input."""
    entry_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entry).get(entry_id)
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
        # entry.tags = request.POST['tags']
        entry.body = request.POST['body']
        request.dbsession.add(entry)
        request.dbsession.flush()
        return HTTPFound(request.route_url('update_article_page', id=entry.id))


@view_config(
    route_name='verify_delete',
    renderer='../templates/delete_view.jinja2')
def verify_delete(request):
    """Renders delete view using the post id to prepare to delete
    and requests password."""
    entry_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entry).get(entry_id)
    if request.method == "GET":
        return {
            "id": entry.id,
            "title": entry.title,
            "date": entry.date,
            "tags": entry.tags,
            "body": entry.body
            }
    if request.method == "POST":
        password = request.POST['password']
        if password == "top_secret_password":
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
