import pytest
from flask import g, get_flashed_messages, url_for
from flask_login.test_client import FlaskLoginClient
from flaskbb.extensions import db
from flaskbb.forum.models import Forum, Post, Topic
from flaskbb.plugins.models import PluginRegistry
from flaskbb.settings import Setting
from sqlalchemy import event

from portal import SETTINGS, views


def test_index_redirects_to_the_forum_when_the_plugin_is_not_registered(
    application, default_settings
):
    with application.test_request_context():
        response = views.index()
        messages = get_flashed_messages(with_categories=True)
        forum_index = url_for("forum.index")

    assert response.status_code == 302
    assert response.headers["Location"] == forum_index
    assert (
        "warning",
        "Plugin 'portal' could not be found in the plugin registry.",
    ) in messages


@pytest.fixture
def client(application, default_settings, default_groups, monkeypatch):
    # FlaskLoginClient doesn't store the session identifier, so "basic"
    # session protection would mark every login as stale on the first request
    monkeypatch.setattr(application.login_manager, "session_protection", None)
    monkeypatch.setattr(application, "test_client_class", FlaskLoginClient)

    def make(user=None):
        g.pop("_login_user", None)
        return application.test_client(user=user)

    yield make
    g.pop("_login_user", None)


@pytest.fixture
def queries():
    statements = []

    def record(conn, cursor, statement, parameters, context, executemany):
        statements.append(statement)

    event.listen(db.engine, "before_cursor_execute", record)
    yield statements
    event.remove(db.engine, "before_cursor_execute", record)


@pytest.fixture
def installed_portal(default_settings):
    registry = PluginRegistry(name="portal")
    registry.enabled = True
    registry.save()
    Setting.install_group(SETTINGS.key)

    def configure(**values):
        Setting.update(SETTINGS.key, values)

    return configure


def _forum(category, default_groups, title):
    forum = Forum(title=title, category_id=category.id)
    forum.groups = default_groups
    return forum.save()


def _topic(forum, user, title):
    return Topic(title=title).save(forum=forum, user=user, post=Post(content=f"**{title}**"))


def _measure(client, queries):
    """Queries of a repeat visit, with the session emptied like at the start of a request."""
    client.get("/portal/")
    db.session.expire_all()
    queries.clear()
    resp = client.get("/portal/")
    assert resp.status_code == 200
    return resp, sum(1 for statement in queries if "posts" in statement or "forums" in statement)


def test_index_shows_news_from_the_configured_forums_only(
    client, user, category, default_groups, installed_portal
):
    news_forum = _forum(category, default_groups, "News")
    other_forum = _forum(category, default_groups, "Other")
    _topic(news_forum, user, "Announcement")
    _topic(other_forum, user, "Chatter")
    installed_portal(FORUM_IDS=[news_forum.id], RECENT_TOPICS=1)

    resp = client(user).get("/portal/")

    assert b"<strong>Announcement</strong>" in resp.data
    assert b"<strong>Chatter</strong>" not in resp.data
    assert b">Announcement</a>" in resp.data
    assert b">Chatter</a>" in resp.data
    assert resp.data.count(b'class="portal-topic"') == 1


def test_index_query_count_does_not_grow_with_forums_and_topics(
    client, user, category, default_groups, installed_portal, queries
):
    news_forum = _forum(category, default_groups, "News")
    _topic(news_forum, user, "first")
    installed_portal(FORUM_IDS=[news_forum.id])
    viewer = client(user)
    _, with_one_topic = _measure(viewer, queries)

    for i in range(5):
        _topic(_forum(category, default_groups, f"Forum {i}"), user, f"elsewhere {i}")
    for i in range(8):
        _topic(news_forum, user, f"news {i}")

    resp, with_many_topics = _measure(viewer, queries)

    assert with_many_topics == with_one_topic
    assert b"<strong>news 7</strong>" in resp.data
    assert b">elsewhere 4</a>" in resp.data
