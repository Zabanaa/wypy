from wypy.wypy import WyPy
from wypy.general import General
from wypy.device import Device
from wypy.networking import Network
import pytest


@pytest.fixture(scope='function')
def general():
    general = General()
    yield general


@pytest.fixture(scope='function')
def wypy():
    wypy = WyPy()
    yield wypy


@pytest.fixture(scope='function')
def device():
    device = Device()
    yield device


@pytest.fixture(scope='function')
def network():
    network = Network()
    yield network
