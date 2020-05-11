import json
import datetime
from collections import deque

UNDEFINED = 'UNDEFINED'
FIX_STATUS_VALUES = ['proposed', 'rejected', 'accepted', 'withdrawn']

def is_undefined(x):
    if x and x != UNDEFINED:
        return True

    return False


def nested_lookup(key_path, item, must_exist=False):
    not_found = '__NOT_FOUND__'

    for key in key_path.split('.'):
        if type(item) == dict:
            item = item.get(key, not_found)
        else:
            item = not_found

        if item == not_found:
            if must_exist:
                raise KeyError(f'Required content "{key}" not found.')
            return None

    return item


def now_string():
    return datetime.datetime.now().isoformat().split('.')[0]


class JDict(dict):

    def _tostring(self, obj):
        return json.dumps(obj)

    def __setitem__(self, key, value):
        jkey = self._tostring(key)
        super().__setitem__(jkey, value)

    def __getitem__(self, key):
        jkey = self._tostring(key)
        return super().__getitem__(jkey)

    def __delitem__(self, key):
        jkey = self._tostring(key)
        super().__delitem__(jkey)

    def __contains__(self, key):
        jkey = self._tostring(key)
        return super().__contains__(jkey)

    def keys(self):
        return [json.loads(_) for _ in super().keys()]

    def setdefault(self, key, default):
        jkey = self._tostring(key)
        return super().setdefault(jkey, default)


def is_subsequence(s1, s2):
    """
    Returns True if s1 is a sub-sequence of s2. All elements in s1 must
    exist in s2 and be found in the same order. s2 can include additional
    items that are not in s1.
    :param s1: sub-sequence [sequence]
    :param s2: main sequence [sequence]
    :return: Boolean
    """
    # Convert to deque so that we can popleft() items
    s1 = deque(s1)
    for i in s2:
        if i == s1[0]:
            s1.popleft()
        if not s1:
            return True
    return False


def get_extra_items_in_larger_sequence(small, large):
    """
    Returns a list of items found only in sequence `large`.
    :param small: sub-sequence [sequence]
    :param large: main sequence [sequence]
    :return: list or False (if not subsequence)
    """
    if not is_subsequence(small, large):
        return None
    # Convert to deque so that we can popleft() items
    small = deque(small)
    large = deque(large)
    excess = []
    while large:
        item = large.popleft()
        if item not in small:
            excess.append(item)
    return excess
