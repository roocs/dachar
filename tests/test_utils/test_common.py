from dachar.utils.common import JDict, get_extra_items_in_larger_sequence, is_subsequence, nested_lookup


def test_jdict():
    bkey = {'a': 1, 'b': 2}
    d = JDict()

    d[bkey] = 'hi'
    assert (d[bkey] == 'hi')

    del d[bkey]
    assert (bkey not in d)

    d.setdefault({'c': 23}, [])


def test_get_extra_items_in_larger_sequence():
    large = [('time', 12), ('level', 1)]
    small = [('time', 12)]
    res = get_extra_items_in_larger_sequence(small, large)
    assert (res == [large[1]])


def test_get_items_larger_sequence_2():
    large = ['lev', 'time']
    small = ['time']
    res = get_extra_items_in_larger_sequence(small, large)
    assert (res == [large[0]])


def test_get_items_larger_sequence_3():
    large = [3540, 1]
    small = [3540]
    res = get_extra_items_in_larger_sequence(small, large)
    assert (res == [large[1]])


def test_get_items_larger_sequence_4():
    large = [('time', 3600), ('realisation', 1), ('level', 1)]
    small = [('time', 3600)]
    res = get_extra_items_in_larger_sequence(small, large)
    assert (res == large[1:])


def test_get_items_larger_sequence_5():
    large = [('time', 3600), ('level', 1)]
    small = [('realisation', 1)]
    res = get_extra_items_in_larger_sequence(small, large)
    assert (res is None)

# expect None because small isn't a subset
def test_get_items_larger_sequence_6():
    large = ['i', 'j', 'latitude', 'longitude', 'time', 'type']
    small = ['latitude', 'longitude', 'time', 'x', 'y']
    res = get_extra_items_in_larger_sequence(small, large)
    assert (res is None)


def test_nested_lookup():
    item = {
        "coordinates": {
            "i": {
                "id": "i",
            },
            "j": {
                "id": "j",
            },
            "latitude": {
                "id": "latitude",
            },
            "longitude": {
                "id": "longitude",
            },
            "time": {
                "id": "time",
            },
            "type": {
                "id": "type",
            }
        }}
    lookup = nested_lookup('coordinates.*.id', item, must_exist=True)
    assert lookup == ['i', 'j', 'latitude', 'longitude', 'time', 'type']
