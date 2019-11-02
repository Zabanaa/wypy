from wypy.general import General
from wypy.networking import Network
import pytest


@pytest.fixture(scope='function')
def general():
    general = General()
    yield general


@pytest.fixture(scope='function')
def network():
    network = Network()
    yield network
