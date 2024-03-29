import pytest
import xarray as xr

from tests._common import MINI_ESGF_MASTER_DIR

test_path1 = f"{MINI_ESGF_MASTER_DIR}/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc"

test_path2 = (
    f"{MINI_ESGF_MASTER_DIR}/test_data/gws/nopw/j04/cp4cds1_vol1/data/c3s-cordex/output/EUR-11/IPSL/MOHC-HadGEM2-ES/"
    "rcp85/r1i1p1/IPSL-WRF381P/v1/day/psl/v20190212/*.nc"
)

test_path3 = f"{MINI_ESGF_MASTER_DIR}/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/latest/rh/*.nc"


# testing whether outputs of da.coords and da.dims are the same
def test_coord_keys_and_dims_1(load_esgf_test_data):
    ds = xr.open_mfdataset(test_path1, use_cftime=True, combine="by_coords")
    da = ds["tas"]

    with pytest.raises(AssertionError):
        assert set(da.coords.keys()) == set(da.dims)
    with pytest.raises(AssertionError):
        assert sorted(da.shape) == sorted(
            [da[f"{coord}"].size for coord in da.coords.keys()]
        )


def test_coord_keys_and_dims_2(load_esgf_test_data):
    ds = xr.open_mfdataset(test_path2, use_cftime=True, combine="by_coords")
    da = ds["psl"]

    with pytest.raises(AssertionError):
        assert set(da.coords.keys()) == set(da.dims)
    with pytest.raises(AssertionError):
        assert sorted(da.shape) == sorted(
            [da[f"{coord}"].size for coord in da.coords.keys()]
        )


# in some cases they can be the same
def test_coord_keys_and_dims_3(load_esgf_test_data):
    ds = xr.open_mfdataset(test_path3, use_cftime=True, combine="by_coords")
    da = ds["rh"]

    assert set(da.coords.keys()) == set(da.dims)
    assert sorted(da.shape) == sorted(
        [da[f"{coord}"].size for coord in da.coords.keys()]
    )
