from pyramid.view import notfound_view_config
from pyramid.view import forbidden_view_config


@notfound_view_config(renderer='../templates/404.jinja2')
def notfound_view(request):
    request.response.status = 404
    return {}


@forbidden_view_config(renderer='../templates/403.jinja2')
def forbidden(request):
    request.response.status = 403
    return {}

