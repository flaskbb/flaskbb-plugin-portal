# -*- coding: utf-8 -*-
"""
flaskbb.plugins.portal.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the portal view.

:copyright: (c) 2014 by the FlaskBB Team.
:license: BSD, see LICENSE for more details.
"""

from flask import Blueprint, current_app, flash, request
from flask_babelplus import gettext as _
from flask_login import current_user
from flaskbb.extensions import db
from flaskbb.forum.models import Forum, Post, Topic
from flaskbb.plugins.models import PluginRegistry
from flaskbb.user.models import Group, User
from flaskbb.utils.helpers import get_online_users, render_template, time_diff
from flaskbb.utils.settings import flaskbb_config
from sqlalchemy import select

portal = Blueprint("portal", __name__, template_folder="templates")


@portal.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    forum_ids = []

    plugin = PluginRegistry.get_by(name="portal")
    if plugin and not plugin.settings:
        flash(
            _(
                "Please install the plugin first to configure the forums "
                "which should be displayed."
            ),
            "warning",
        )
    else:
        forum_ids: list[int] = plugin.settings["forum_ids"]
    group_ids = [group.id for group in current_user.groups]

    forums = (
        db.session.execute(
            select(Forum).where(
                Forum.groups.any(Group.id.in_(group_ids)), Forum.id.in_(forum_ids)
            )
        )
        .scalars()
        .unique()
    )

    # get the news forums - check for permissions
    news_ids = [f.id for f in forums]
    news = db.paginate(
        select(Topic).where(Topic.forum_id.in_(news_ids)).order_by(Topic.id.desc()),
        page=page,
        per_page=flaskbb_config["TOPICS_PER_PAGE"],
        error_out=True,
    )

    # get the recent topics from all to the user available forums (not just the
    # configured ones)
    all_forums = (
        db.session.execute(
            select(Forum).where(Forum.groups.any(Group.id.in_(group_ids)))
        )
        .scalars()
        .unique()
    )
    all_ids = [f.id for f in all_forums]
    recent_topics = db.session.execute(
        select(Topic)
        .where(Topic.forum_id.in_(all_ids))
        .order_by(Topic.last_updated.desc())
        .limit(plugin.settings.get("recent_topics", 10))
    ).scalars()

    user_count = User.count()
    topic_count = Topic.count()
    post_count = Post.count()
    newest_user = db.session.execute(select(User).order_by(User.id.desc())).scalar()

    # Check if we use redis or not
    if not current_app.config["REDIS_ENABLED"]:
        online_users = User.count(clause=[User.lastseen >= time_diff()])
        online_guests = None
    else:
        online_users = len(get_online_users())
        online_guests = len(get_online_users(guest=True))

    return render_template(
        "index.html",
        news=news,
        recent_topics=recent_topics,
        user_count=user_count,
        topic_count=topic_count,
        post_count=post_count,
        newest_user=newest_user,
        online_guests=online_guests,
        online_users=online_users,
    )
