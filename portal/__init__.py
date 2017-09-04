# -*- coding: utf-8 -*-
"""
    flaskbb.plugins.portal
    ~~~~~~~~~~~~~~~~~~~~~~

    A Portal Plugin for FlaskBB.

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
from flaskbb.forum.models import Forum


def available_forums():
    forums = Forum.query.order_by(Forum.id.asc()).all()
    return [(forum.id, forum.title) for forum in forums]


SETTINGS = {
    'forum_ids': {
        'value': [1],
        'value_type': "selectmultiple",
        'name': "Forum IDs",
        'description': ("The forum ids from which forums the posts "
                        "should be displayed on the portal."),
        'extra': {"choices": available_forums, "coerce": int}
    },
    'recent_topics': {
        'value': 10,
        'value_type': "integer",
        'name': "Number of Recent Topics",
        'description': "The number of topics in Recent Topics.",
        'extra': {"min": 1},
    },
}
