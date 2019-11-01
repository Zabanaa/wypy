from wypy.general import General
import pytest


@pytest.fixture(scope='function')
def general():
    general = General()
    yield general
