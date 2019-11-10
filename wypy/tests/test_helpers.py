from wypy.utils.helpers import (
    is_valid_uuid,
    format_list,
    format_table_key
)


def test_format_list():
    addresses = [
        {'address': '192.168.0.1'},
        {'address': '192.168.0.2'},
        {'address': '192.168.0.3'},
    ]
    result = format_list(addresses)
    expected_result = '192.168.0.1 - 192.168.0.2 - 192.168.0.3'
    assert result == expected_result

    domains = [
        {'age': 23, 'name': 'karim'},
        {'age': 24, 'name': 'hatem'},
        {'age': 25, 'name': 'samir'}
    ]
    result = format_list(domains, key='name')
    expected_result = 'karim - hatem - samir'
    assert result == expected_result

    empty_list = []
    result = format_list(empty_list)
    assert result == '--'


def test_format_table_key():
    key = 'ipv4_address'
    assert format_table_key(key) == 'IPV4 ADDRESS'

    key = 'hello'
    assert format_table_key(key) == 'HELLO'


def test_is_valid_uuid():
    _str = 'kwjkewe'
    assert is_valid_uuid(_str) == False

    _str = '67a548de-8383-4330-abf8-ce60544c5366'
    assert is_valid_uuid(_str) == True
