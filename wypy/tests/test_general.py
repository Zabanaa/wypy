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
    Assert General._translate_status_code returns the
    correct string for the WIFI property.
    """
    prop = 'WIFI'

    result = general._translate_status_code(prop, 1)
    assert result == colored('enabled', 'green')

    result = general._translate_status_code(prop, 0)
    assert result == colored('disabled', 'red')


def test_translate_status_code_state(general):
    """
    Assert General._translate_status_code returns the
    correct string for the STATE property.
    """
    prop = 'STATE'

    result = general._translate_status_code(prop, 70)
    assert result == colored('connected', 'green')

    result = general._translate_status_code(prop, 60)
    assert result == colored('connected (site)', 'green')

    result = general._translate_status_code(prop, 50)
    assert result == colored('connected (local)', 'green')

    result = general._translate_status_code(prop, 40)
    assert result == colored('connecting', 'yellow')

    result = general._translate_status_code(prop, 30)
    assert result == colored('disconnecting', 'red')

    result = general._translate_status_code(prop, 20)
    assert result == colored('disconnected', 'red')

    result = general._translate_status_code(prop, 10)
    assert result == colored('asleep', 'yellow')

    result = general._translate_status_code(prop, 0)
    assert result == colored('unknown', 'red')


def test_get_status_info(general, mocker):
    """
    Assert General.get_status_info calls the get_object_property
    method as many times as there are status_properties,
    each time passing the correct argument.
    """
    calls = [mock.call(prop) for prop in general.status_properties]
    mock_get_prop = mocker.patch.object(general, 'get_object_property')
    general._get_status_info()
    mock_get_prop.assert_has_calls(calls, any_order=True)


def test_get_hostname(general, mocker):
    """
    Assert General.get_hostname calls the get_object_property method
    with 'Hostname' as the argument.
    """
    mock_hostname = 'some hostname'
    mock_get_prop = mocker.patch.object(general, 'get_object_property', return_value=mock_hostname)
    mock_click_echo = mocker.patch('click.echo')
    general.get_hostname()
    mock_get_prop.assert_called_once_with('Hostname')
    mock_click_echo.assert_called_once_with(f'Hostname: {mock_hostname}')
