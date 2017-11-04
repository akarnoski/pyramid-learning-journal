from pyramid.response import Response
import os


HERE = os.path.abspath(__file__)
DATA = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'data')
TEMPLATES = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'templates')


def list_view(request):
    """Response that renders index.html view."""
    with open(os.path.join(TEMPLATES, 'index.html')) as file:
        return Response(file.read())


def detail_view(request):
    """Renders the detail page."""
    with open(os.path.join(DATA, 'oct30.html')) as file:
        return Response(file.read())


def create_view(request):
    """Renders the new entry page."""
    with open(os.path.join(TEMPLATES, 'form_page.html')) as file:
        return Response(file.read())


def update_view(request):
    """Renders the page for updating existing articles."""
    with open(os.path.join(TEMPLATES, 'edit_page.html')) as file:
        return Response(file.read())
