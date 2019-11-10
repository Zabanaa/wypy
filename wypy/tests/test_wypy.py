from termcolor import colored


def test_translate_status_code_connectivity(wypy):
    """
    Assert General.translate_status_code method returns the
    correct string for the CONNECTIVITY property.
    """
    prop = 'CONNECTIVITY'

    result = wypy.translate_status_code(prop, 4)
    assert result == colored('full', 'green')

    result = wypy.translate_status_code(prop, 3)
    assert result == colored('limited', 'green')

    result = wypy.translate_status_code(prop, 2)
    assert result == colored('portal', 'yellow')

    result = wypy.translate_status_code(prop, 1)
    assert result == colored('none', 'red')

    result = wypy.translate_status_code(prop, 0)
    assert result == colored('unknown', 'red')


def test_translate_status_code_wifi(wypy):
    """
    Assert General.translate_status_code returns the
    correct string for the WIFI property.
    """
    prop = 'WIFI'

    result = wypy.translate_status_code(prop, 1)
    assert result == colored('enabled', 'green')

    result = wypy.translate_status_code(prop, 0)
    assert result == colored('disabled', 'red')


def test_translate_status_code_state(wypy):
    """
    Assert General.translate_status_code returns the
    correct string for the STATE property.
    """
    prop = 'STATE'

    result = wypy.translate_status_code(prop, 70)
    assert result == colored('connected', 'green')

    result = wypy.translate_status_code(prop, 60)
    assert result == colored('connected (site)', 'green')

    result = wypy.translate_status_code(prop, 50)
    assert result == colored('connected (local)', 'green')

    result = wypy.translate_status_code(prop, 40)
    assert result == colored('connecting', 'yellow')

    result = wypy.translate_status_code(prop, 30)
    assert result == colored('disconnecting', 'red')

    result = wypy.translate_status_code(prop, 20)
    assert result == colored('disconnected', 'red')

    result = wypy.translate_status_code(prop, 10)
    assert result == colored('asleep', 'yellow')

    result = wypy.translate_status_code(prop, 0)
    assert result == colored('unknown', 'red')

