from collections import MutableMapping
from uuid import UUID


def flatten(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def is_valid_uuid(_str):
    """
    Checks if _str is a uuidv4 string
    return <bool> - Whether the string is a uuid
    """
    try:
        UUID(_str, version=4)
    except ValueError:
        return False
    else:
        return True


def format_list(data_list, key='address'):
    """
    this function will map over a given list of dictionaries,
    extract all instances dict[key] and join the
    result into a final string.

    It's particularly useful when joining lists of ip addresses
    and domain names.

    If the case `data_list` is empty, the function will simply return: '--'.
    """

    if len(data_list) == 0:
        return '--'
    # TODO: wrap this call in a try / except block
    ips = list(map(lambda x: str(x[key]), data_list))
    return ' - '.join(ips)


def format_table_key(key):
    """
    Accepts a string as the only argument
    replaces underscores with spaces and uppercases the string
    """
    return key.upper().replace('_', ' ')


def format_connection_name(name):
    """
        Takes a connection name and replaces
        every space with an underscore.
    """
    return name.replace(' ', '_')


def user_choice_to_bool(choice):
    """

    Arguments:
        choice {[string]} -- [the choice the user was prompted to make]

    Returns:
        [boolean] -- [the choice]
    """
    return True if choice == 'yes' else False
