from unittest import mock
from termcolor import colored


def test_show_status(general):
    """
    Assert that General.show_status effectively makes calls to
    the following private methods:

        _get_status_info
        _translate_status_code

    Both of which are being mocked.
    This test also asserts that _translate_status_code was called 6 times.
    """

    props = general.property_names
    statuses = [70, 4, 1, 1, 1, 1]
    calls = [mock.call(name, status) for name, status in zip(props, statuses)]
    with mock.patch.object(general, '_get_status_info', return_value=statuses) as mock_gen:
        with mock.patch.object(general, '_translate_status_code') as mock_translate:
            general.show_status()
        mock_translate.assert_has_calls(calls, any_order=True)
    mock_gen.assert_called_once()


def test_translate_status_code_connectivity(general):
    """ 
    Assert General._translate_status_code method returns the 
    correct string for the CONNECTIVITY property.
    ""[summary]
    """
    prop = 'CONNECTIVITY'

    result = general._translate_status_code(prop, 4)
    assert result == colored('full', 'green')

    result = general._translate_status_code(prop, 3)
    assert result == colored('limited', 'green')

    result = general._translate_status_code(prop, 2)
    assert result == colored('portal', 'yellow')

    result = general._translate_status_code(prop, 1)
    assert result == colored('none', 'red')

    result = general._translate_status_code(prop, 0)
    assert result == colored('unknown', 'red')


def test_translate_status_code_wifi(general):
    """ 
    Assert General._translate_status_code method returns the 
    correct string for the CONNECTIVITY property.
    ""[summary]
    """
    prop = 'WIFI'

    result = general._translate_status_code(prop, 1)
    assert result == colored('enabled', 'green')

    result = general._translate_status_code(prop, 0)
    assert result == colored('disabled', 'red')
