import pytest
from flaskbb.settings import setting_registry
from tests.fixtures.app import *
from tests.fixtures.forum import *
from tests.fixtures.user import *

from portal import SETTINGS


@pytest.fixture(scope="package", autouse=True)
def _register_portal_settings(application):
    """Normally done by create_app() for an entry-point installed plugin."""
    if not setting_registry.is_plugin_group(SETTINGS.key):
        setting_registry.register_group(SETTINGS, is_plugin=True)
