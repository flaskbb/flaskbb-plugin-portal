# -*- coding: utf-8 -*-
"""
    flaskbb.plugins.portal
    ~~~~~~~~~~~~~~~~~~~~~~

    A Portal Plugin for FlaskBB.

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
import os

from pluggy import HookimplMarker

from flaskbb.forum.models import Forum
from flaskbb.utils.forms import SettingValueType
from flaskbb.utils.helpers import render_template

from .views import portal

__version__ = "1.1.3"


hookimpl = HookimplMarker("flaskbb")


def available_forums():
    forums = Forum.query.order_by(Forum.id.asc()).all()
    return [(forum.id, forum.title) for forum in forums]


@hookimpl
def flaskbb_load_migrations():
    return os.path.join(os.path.dirname(__file__), "migrations")


@hookimpl
def flaskbb_load_translations():
    return os.path.join(os.path.dirname(__file__), "translations")


@hookimpl
def flaskbb_load_blueprints(app):
    app.register_blueprint(
        portal, url_prefix=app.config.get("PLUGIN_PORTAL_URL_PREFIX", "/portal")
    )


@hookimpl
def flaskbb_tpl_navigation_before():
    return render_template("navigation_snippet.html")


SETTINGS = {
    "forum_ids": {
        "value": [1],
        "value_type": SettingValueType.selectmultiple,
        "name": "Forum IDs",
        "description": (
            "The forum ids from which forums the posts "
            "should be displayed on the portal."
        ),
        "extra": {"choices": available_forums, "coerce": int},
    },
    "recent_topics": {
        "value": 10,
        "value_type": SettingValueType.integer,
        "name": "Number of Recent Topics",
        "description": "The number of topics in Recent Topics.",
        "extra": {"min": 1},
    },
}
