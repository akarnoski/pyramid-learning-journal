"""pytest fixture."""
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

    Every test that includes this fixture will add new random entries.
    """
    dummy_request.dbsession.add_all(FAKE_ENTRIES)


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


@pytest.fixture
def empty_db(testapp):
    """Tear down the database and add a fresh table."""
    SessionFactory = testapp.app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


fake = Faker()
FAKE_ENTRIES = [Entry(
    title=fake.job(),
    date=fake.century(),
    tags=fake.job(),
    body=fake.text()
) for i in range(20)]
