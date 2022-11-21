import pytest
from website import create_app, drop_database

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here
    drop_database(app)


@pytest.fixture()
def client(app):
    return app.test_client()


# @pytest.fixture()
# def runner(app):
#     return app.test_cli_runner()