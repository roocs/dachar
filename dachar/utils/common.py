import json
import datetime

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

    def setdefault(self, key, default):
        jkey = self._tostring(key)
        return super().setdefault(jkey, default)
