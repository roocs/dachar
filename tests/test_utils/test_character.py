import xarray as xr

test_path = 'tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5' \
            '/output1/INM/inmcm4/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*.nc'


def test_order_of_coords():
    ds = xr.open_mfdataset(test_path, use_cftime=True, combine='by_coords')
    da = ds['zostoga']

    coords = [_ for _ in da.coords]
    assert coords == ['lev', 'time']

    coord_names_keys = [_ for _ in da.coords.keys()]
    assert coord_names_keys == ['lev', 'time']

    # this changes order each time
    # coord_names = [_ for _ in da.coords._names]
    # assert coord_names == ['time', 'lev']

    coord_names_keys = [_ for _ in da.coords]
    assert coord_names_keys == ['lev', 'time']

    coord_sizes = [da[f'{coord}'].size for coord in da.coords.keys()]
    shape = da.shape

    dims = da.dims
    assert dims == ('time', 'lev')

    assert shape == (1140, 1) # looks like shape comes from dims
    assert coord_sizes == [1, 1140]
    assert ds['lev'].shape == (1,)
    assert ds['time'].shape == (1140,)


# coords: a dict-like container of arrays (coordinates) that label each point
# (e.g., 1-dimensional arrays of numbers, datetime objects or strings)

# http://xarray.pydata.org/en/stable/data-structures.html


# in character extractor could use
# 'shape': [da[f'{coord}'].size for coord in da.coords.keys()],
# 'coord_names': [_ for _ in da.coords.keys()]

# or

# 'shape': da.shape,
# 'coord_names': da.dims

