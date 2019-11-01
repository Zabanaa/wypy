from termcolor import colored


def test_translate_status_code_connectivity(general):
    """
    Assert General._translate_status_code method returns the
    correct string for the CONNECTIVITY property.
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
