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


def test_get_items_larger_sequence_6():
    large = ['i', 'j', 'latitude', 'longitude', 'time', 'type']
    small = ['latitude', 'longitude', 'time', 'x', 'y']
    res = get_extra_items_in_larger_sequence(small, large)
    assert (res == [large[-1]])


# typical content: {'data.coord_names': ['time'], 'data.shape': [3540]}

# atypical content: [{'data.coord_names': ['lev', 'time'], 'data.shape': [1, 1140]}, {'data.coord_names': ['time'], 'data.shape': [3529]}, {'data.coord_names': ['time'], 'data.shape': [360]}]


def test_nested_lookup():
    item = {
        "coordinates": {
            "i": {
                "id": "i",
                "length": 9,
                "long_name": "cell index along first dimension",
                "max": 800.0,
                "min": 0.0,
                "units": "1"
            },
            "j": {
                "id": "j",
                "length": 5,
                "long_name": "cell index along second dimension",
                "max": 400.0,
                "min": 0.0,
                "units": "1"
            },
            "latitude": {
                "bounds": "vertices_latitude",
                "id": "latitude",
                "length": 5,
                "long_name": "latitude",
                "max": 89.41692821142533,
                "min": -77.54309917089314,
                "standard_name": "latitude",
                "units": "degrees_north"
            },
            "longitude": {
                "bounds": "vertices_longitude",
                "id": "longitude",
                "length": 5,
                "long_name": "longitude",
                "max": 352.8538802939694,
                "min": 7.451098374047184,
                "standard_name": "longitude",
                "units": "degrees_east"
            },
            "time": {
                "axis": "T",
                "bounds": "time_bnds",
                "calendar": "proleptic_gregorian",
                "id": "time",
                "length": 1980,
                "long_name": "time",
                "max": "2014-12-16T12:00:00",
                "min": "1850-01-16T12:00:00",
                "standard_name": "time"
            },
            "type": {
                "dtype": "|S7",
                "id": "type",
                "length": 1,
                "long_name": "Sea Ice area type",
                "standard_name": "area_type",
                "value": "sea_ice"
            }
        }}
    lookup = nested_lookup('coordinates.*.id', item, must_exist=True)
    assert lookup == ['i', 'j', 'latitude', 'longitude', 'time', 'type']
