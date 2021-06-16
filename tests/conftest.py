import os
from datetime import datetime
from datetime import timedelta

import pytest
from git import Repo
from netCDF4 import Dataset
from netCDF4 import date2num

from tests._common import MINI_ESGF_CACHE_DIR
from tests._common import write_roocs_cfg

write_roocs_cfg()


ESGF_TEST_DATA_REPO_URL = "https://github.com/roocs/mini-esgf-data"


# Fixture to load mini-esgf-data repository used by roocs tests
@pytest.fixture
def load_esgf_test_data():
    """
    This fixture ensures that the required test data repository
    has been cloned to the cache directory within the home directory.
    """
    branch = "master"
    target = os.path.join(MINI_ESGF_CACHE_DIR, branch)

    if not os.path.isdir(MINI_ESGF_CACHE_DIR):
        os.makedirs(MINI_ESGF_CACHE_DIR)

    if not os.path.isdir(target):
        repo = Repo.clone_from(ESGF_TEST_DATA_REPO_URL, target)
        repo.git.checkout(branch)

    elif os.environ.get("ROOCS_AUTO_UPDATE_TEST_DATA", "true").lower() != "false":
        repo = Repo(target)
        repo.git.checkout(branch)
        repo.remotes[0].pull()


@pytest.fixture
def create_netcdf_file():
    if not os.path.exists("test/data"):
        os.makedirs("test/data")

    if not os.path.exists("test/data/test_file.nc"):
        p = os.path.join("test/data", "test_file.nc")
        test_file = Dataset(p, "w", format="NETCDF4")
        test_file.createDimension("lat", 145)
        lat = test_file.createVariable("lat", "f4", ("lat",))
        test_file.createDimension("lon", 192)
        lon = test_file.createVariable("lon", "f4", ("lon",))
        lats = np.arange(-90, 91, 1.25)
        lons = np.arange(0, 360, 1.875)
        lat[:] = lats
        lon[:] = lons
        test_file.createDimension("time", 876)
        times = test_file.createVariable("time", "f8", ("time",))
        times.units = "hours since 0001-01-01 00:00:00.0"
        times.calendar = "gregorian"
        dates = [datetime(2001, 3, 1) + n * timedelta(hours=12) for n in range(876)]
        times[:] = date2num(dates, units=times.units, calendar=times.calendar)
        temp = test_file.createVariable("temp", "f4", ("time", "lat", "lon",))
        temp.units = "K"
    return "test/data/test_file.nc"


@pytest.fixture
def create_netcdf_file_2():
    if not os.path.exists("test/data"):
        os.makedirs("test/data")

    if not os.path.exists("test/data/test_file_2.nc"):
        p = os.path.join("test/data", "test_file_2.nc")
        test_file_2 = Dataset(p, "w", format="NETCDF4")
        test_file_2.createDimension("lat", 145)
        lat = test_file_2.createVariable("lat", "f4", ("lat",))
        test_file_2.createDimension("lon", 192)
        lon = test_file_2.createVariable("lon", "f4", ("lon",))
        lats = np.arange(-90, 91, 1.25) + 1
        lons = np.arange(0, 360, 1.875) + 1
        lat[:] = lats
        lon[:] = lons
        test_file_2.createDimension("time", 876)
        times = test_file_2.createVariable("time", "f8", ("time",))
        times.units = "hours since 0001-01-01 00:00:00.0"
        times.calendar = "gregorian"
        dates = [datetime(2003, 7, 26) + n * timedelta(hours=12) for n in range(876)]
        times[:] = date2num(dates, units=times.units, calendar=times.calendar)
        temp = test_file_2.createVariable("temp", "f4", ("time", "lat", "lon",))
        temp.units = "K"

    return "test/data/test_file_2.nc"
