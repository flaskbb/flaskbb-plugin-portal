import pytest
from tests.fixtures.app import *
from tests.fixtures.forum import *
from tests.fixtures.user import *


@pytest.fixture(scope="package")
def tested_plugins():
    return ["portal"]
