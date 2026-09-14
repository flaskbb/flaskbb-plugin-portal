from flask import get_flashed_messages, url_for

from portal import views


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
