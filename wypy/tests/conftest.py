from wypy.utils.constants import NM_BUS_NAME, NM_OBJ_PATH, NM_IFACE
from wypy.general import General
import pytest


@pytest.fixture(scope='function')
def general():
    general = General(NM_BUS_NAME, NM_OBJ_PATH, NM_IFACE)
    yield general
