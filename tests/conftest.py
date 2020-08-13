import os
from datetime import datetime
from datetime import timedelta

import numpy as np
import pytest
from netCDF4 import Dataset
from netCDF4 import date2num
from netCDF4 import num2date
from unittest import mock

from tests._common import get_tests_project_base_dir
from unittest import mock


@pytest.fixture(scope="session", autouse=True)
def mock_base_dirs_scan():
    with mock.patch(
        "dachar.scan.scan.get_project_base_dir", side_effect=get_tests_project_base_dir
    ):
        yield


@pytest.fixture(scope="session", autouse=True)
def mock_base_dirs_switch_ds():
    with mock.patch(
        "dachar.utils.switch_ds.get_project_base_dir", side_effect=get_tests_project_base_dir
    ):
        yield
        
        
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
