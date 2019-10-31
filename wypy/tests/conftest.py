from wypy.utils.constants import NM_OBJ_PATH
from wypy.general import General
import pytest


@pytest.fixture(scope='function')
def general():
    general = General(NM_OBJ_PATH)
    yield general
