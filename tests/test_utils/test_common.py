from dachar.utils.common import JDict


def test_jdict():
    bkey = {'a': 1, 'b': 2}
    d = JDict()

    d[bkey] = 'hi'
    assert(d[bkey] == 'hi')

    del d[bkey]
    assert(bkey not in d)

    d.setdefault({'c': 23}, [])


