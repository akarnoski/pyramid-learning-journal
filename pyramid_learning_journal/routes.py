"""Create routes and static views to handle routing configuration."""


def includeme(config):
    """Define the route or view using configurator object."""
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('detail_page', '/journal/{id:\d+}')
    config.add_route('create_article_page', '/journal/new-entry')
    config.add_route('update_article_page', '/journal/{id:\d+}/edit-entry')
    config.add_route('verify_delete', '/journal/{id:\d+}/verification')
    config.add_route('delete_entry', '/journal/{id:\d+}/delete')
    config.add_route('tag_view', '/journal/{tag}')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
