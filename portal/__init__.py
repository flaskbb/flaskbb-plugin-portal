"""
flaskbb.plugins.portal
~~~~~~~~~~~~~~~~~~~~~~

A Portal Plugin for FlaskBB.

:copyright: (c) 2014 by the FlaskBB Team.
:license: BSD, see LICENSE for more details.
"""

import os

from flask import Flask
from flask_babelplus import gettext as _
from flaskbb.display.navigation import NavigationLink
from flaskbb.extensions import db
from flaskbb.forum.models import Forum
from flaskbb.settings import SelectMultipleSetting
from flaskbb.settings.definitions import IntSetting, SettingGroup
from pluggy import HookimplMarker
from sqlalchemy import select

from .views import portal

__version__ = "1.2.0"


hookimpl = HookimplMarker("flaskbb")


def available_forums():
    forums = db.session.execute(select(Forum).order_by(Forum.id.asc())).scalars().unique()
    return [(forum.id, forum.title) for forum in forums]


@hookimpl
def flaskbb_load_migrations():
    return os.path.join(os.path.dirname(__file__), "migrations")


@hookimpl
def flaskbb_load_translations():
    return os.path.join(os.path.dirname(__file__), "translations")


@hookimpl
def flaskbb_load_blueprints(app: Flask):
    app.register_blueprint(portal, url_prefix=app.config.get("PLUGIN_PORTAL_URL_PREFIX", "/portal"))


@hookimpl
def flaskbb_tpl_navigation_before():
    return NavigationLink(
        endpoint="portal.index",
        name=_("Portal"),
        icon="fas fa-home",
    )


impl = HookimplMarker("flaskbb")

SETTINGS = SettingGroup(
    key="portal",
    name="Portal Settings",
    description="Portal settings for your FlaskBB forum.",
    settings=(
        SelectMultipleSetting(
            key="FORUM_IDS",
            value=[1],
            name="Forums",
            description=(
                "The forum ids from which forums the posts should be displayed on the portal."
            ),
            choices=available_forums,
            coerce=int,
        ),
        IntSetting(
            key="RECENT_TOPICS",
            value=10,
            min=1,
            name="Number of Recent Topics",
            description="The number of topics in Recent Topics.",
        ),
    ),
)


@impl
def flaskbb_load_setting_groups():
    return SETTINGS
