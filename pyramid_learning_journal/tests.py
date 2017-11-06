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


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.

    This Configurator instance sets up a pointer to the location of the
        database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.

    This configuration will persist for the entire duration of your PyTest run.
    """
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://localhost:5432/test_learning_journal'
    })
    config.include("pyramid_learning_journal.models")
    config.include('pyramid_learning_journal.routes')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a session for interacting with the test database.
    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Instantiate a fake HTTP Request, complete with a database session.
    This is a function-level fixture, so every new request will have a
    new database session.
    """
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def add_models(dummy_request):
    """Add a bunch of model instances to the database.

    Every test that includes this fixture will add new random expenses.
    """
    dummy_request.dbsession.add_all(FAKE_ENTRIES)


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


@pytest.fixture(scope="session")
def testapp(request):
    from webtest import TestApp
    from pyramid.config import Configurator

    def main():
        settings = {
            'sqlalchemy.url': 'postgres://localhost:5432/test_learning_journal'
        }
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('.models')
        config.include('.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main()

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tearDown)

    return TestApp(app)


@pytest.fixture(scope="session")
def fill_the_db(testapp):
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        dbsession.add_all(FAKE_ENTRIES)

    return dbsession


fake = Faker()
FAKE_ENTRIES = [Entry(
    title=fake.job(),
    date=fake.century(),
    body=fake.text()
) for i in range(20)]


def test_layout_root(testapp, fill_the_db):
    """Test that the contents of the root page contains blog title."""
    response = testapp.get('/', status=200)
    html = response.html
    assert 'Python Learning Journal' in html.find("h1").text


def test_layout_has_correct_article_count(testapp):
    """Test that the contents same number of articles as fake entries."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(FAKE_ENTRIES) == len(html.findAll("article"))


def test_detail_page(testapp):
    """Test the detail page opens without error."""
    response = testapp.get('/journal/5', status=200)
    html = response.html
    assert 'Python Learning Journal' in html.find("h1").text


def test_detail_page_error_opens_404_message(testapp):
    """Test the detail page opens without error."""
    response = testapp.get('/journal/50', status=404)
    html = response.html
    assert '404 Page Not Found' in html.find("p").text


def test_detail_page_renders_post_body(testapp):
    """Test the article body replaced the template expression."""
    response = testapp.get('/journal/7', status=200)
    html = response.html
    assert html.find("p").text != '{{body}}'


def test_create_page(testapp):
    """Test create page renders without error."""
    response = testapp.get('/journal/new-entry', status=200)
    html = response.html
    assert 'Create New Entry' in html.find("h3").text


def test_edit_page(testapp):
    """Test create page renders without error."""
    response = testapp.get('/journal/13/edit-entry', status=200)
    html = response.html
    assert html.find("form")


def test_edit_page(testapp):
    """Test create page renders without error."""
    response = testapp.get('/journal/13/edit-entry', status=200)
    html = response.html
    assert html.find("form")


def test_delete_verification_page(testapp):
    """Test delete verifiation page renders without error."""
    response = testapp.get('/journal/6/verification', status=200)
    html = response.html
    assert html.find("form")


def test_detail_view_raises_error(dummy_request):
    """Test that detail view raises error when id is not found."""
    from pyramid_learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 100
    with pytest.raises(HTTPNotFound):
        response = detail_view(dummy_request)