from pyramid.view import view_config
from pyramid_learning_journal.models.entry import Entry
import pyramid.httpexceptions


@view_config(route_name='home', renderer='../templates/index.jinja2')
def list_view(request):
    entries = request.dbsession.query(Entry).all()
    return {
        "entries": entries
        }


@view_config(route_name='detail_page', renderer='../templates/detail.jinja2')
def detail_view(request):
    the_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entry).get(the_id)
    if entry:
        return {
            "id": entry.id,
            "title": entry.title,
            "date": entry.date,
            "body": entry.body
        }
    else:
        raise HTTPNotFound


@view_config(
    route_name='create_article_page',
    renderer='../templates/form_page.jinja2'
)
def create_view(request):
    return {}


# @view_config(
    # route_name='update_article_page',
    # renderer='../templates/edit_page.jinja2'
# )
# def update_view(request):
#     post_id = int(request.matchdict['id'])
#     if post_id < 0 or post_id > len(JOURNAL_ENTRIES) - 1:
#         raise HTTPNotFound
#     post = list(filter(
#         lambda post: post['id'] == post_id,
#         JOURNAL_ENTRIES)
#     )[0]
#     return {
#         'post': post
#     }
