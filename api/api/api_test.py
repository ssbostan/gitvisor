import pytest
from flask_migrate import upgrade

from api.model import Repository


@pytest.mark.order(0)
def test_env(app):
    assert app.config.get("ENV") == "test"


@pytest.mark.order(0)
def test_debug(app):
    assert app.config.get("DEBUG") is True


@pytest.mark.order(0)
def test_database(app, db):
    with app.app_context():
        assert db.engine.url.database == "test"


@pytest.mark.order(10)
def test_migrate_database(app, mg):
    with app.app_context():
        upgrade()


@pytest.mark.order(100)
def test_seed_database(storage, app, db):
    repository = Repository(
        owner="test",
        url="https://github.com/ssbostan/gitvisor.git",
    )
    with app.app_context():
        db.session.add(repository)
        db.session.commit()
        storage.set("test", repository.id)
    assert type(repr(repository)) is str


@pytest.mark.order(10000)
def test_down_database(app, db):
    with app.app_context():
        db.session.query(Repository).delete()
        db.session.commit()
