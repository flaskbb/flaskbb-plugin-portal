"""
flaskbb.plugins.portal.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the portal view.

:copyright: (c) 2014 by the FlaskBB Team.
:license: BSD, see LICENSE for more details.
"""

from flask import Blueprint, flash, request, url_for
from flask.helpers import redirect
from flask_babelplus import gettext as _
from flask_login import current_user
from flaskbb.extensions import cache, db
from flaskbb.forum.models import Forum, Post, Topic
from flaskbb.plugins.models import PluginRegistry
from flaskbb.settings import flaskbb_config
from flaskbb.user.models import Group, User
from flaskbb.utils.helpers import count_online_users, render_template
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

portal = Blueprint("portal", __name__, template_folder="templates")


@cache.cached(timeout=60, key_prefix="portal_statistics")
def board_statistics() -> dict[str, int]:
    """Counting every post is a full table scan on PostgreSQL, so the
    numbers may lag by a minute."""

    def count_rows(model):
        return select(func.count()).select_from(model).scalar_subquery()

    user_count, topic_count, post_count = db.session.execute(
        select(count_rows(User), count_rows(Topic), count_rows(Post))
    ).one()
    return {"user_count": user_count, "topic_count": topic_count, "post_count": post_count}


@portal.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    forum_ids = []

    plugin = PluginRegistry.get_by(name="portal")
    if not plugin:
        flash(
            _("Plugin 'portal' could not be found in the plugin registry."),
            "warning",
        )
        return redirect(url_for("forum.index"))
    if not plugin.settings:
        flash(
            _("Please install the plugin first to configure the forums which should be displayed."),
            "warning",
        )
    else:
        forum_ids: list[int] = plugin.settings["FORUM_IDS"]
    group_ids = [group.id for group in current_user.groups]

    # every forum the user may see, as plain ids - the news forums are the
    # configured subset of them
    visible_forum_ids = db.session.scalars(
        select(Forum.id).where(Forum.groups.any(Group.id.in_(group_ids)))
    ).all()
    news_forum_ids = set(visible_forum_ids) & set(forum_ids)

    news = db.paginate(
        select(Topic)
        .where(Topic.forum_id.in_(news_forum_ids), Topic.first_post_id.is_not(None))
        .options(selectinload(Topic.first_post))
        .order_by(Topic.id.desc()),
        page=page,
        per_page=flaskbb_config["TOPICS_PER_PAGE"],
        error_out=True,
    )

    recent_topics = db.session.scalars(
        select(Topic)
        .where(Topic.forum_id.in_(visible_forum_ids))
        .order_by(Topic.last_updated.desc())
        .limit(plugin.settings.get("RECENT_TOPICS", 10))
    ).all()

    newest_user = db.session.scalar(select(User).order_by(User.id.desc()).limit(1))
    online_users, online_guests = count_online_users()

    return render_template(
        "portal/index.html",
        news=news,
        recent_topics=recent_topics,
        newest_user=newest_user,
        online_users=online_users,
        online_guests=online_guests,
        **board_statistics(),
    )
