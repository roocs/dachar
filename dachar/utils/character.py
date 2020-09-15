from datetime import datetime

import numpy as np
import xarray as xr
from roocs_utils.xarray_utils import xarray_utils

from dachar import logging

LOGGER = logging.getLogger(__file__)


def get_coords(da):
    """
    E.g.:  ds.['tasmax'].coords.keys()
    KeysView(Coordinates:
    * time     (time) object 2005-12-16 00:00:00 ... 2030-11-16 00:00:00
    * lat      (lat) float64 -90.0 -88.75 -87.5 -86.25 ... 86.25 87.5 88.75 90.0
    * lon      (lon) float64 0.0 1.875 3.75 5.625 7.5 ... 352.5 354.4 356.2 358.1
      height   float64 1.5)


    NOTE: the '*' means it is an INDEX - which means it is a full coordinate variable in NC terms

    Returns a dictionary of coordinate info.
    """

    coords = {}
    LOGGER.debug(f"Found coords: {str(da.coords.keys())}")
    LOGGER.info(f"NOT CAPTURING scalar COORDS BOUND BY coordinates attr yet!!!")

    for coord_id in sorted(da.coords):

        coord = da.coords[coord_id]

        coord_type = xarray_utils.get_coord_type(coord)
        name = coord_type or coord.name
        data = coord.values

        if data.size == 1:
            value = data.tolist()
            if isinstance(value, bytes):
                value = value.decode("utf-8")

            coords[name] = {
                "id": name,
                "value": value,
                "dtype": str(data.dtype),
                "length": 1,
            }

        else:
            mn, mx = data.min(), data.max()

            if coord_type == "time":
                if type(mn) == np.datetime64:
                    mn, mx = [str(_).split(".")[0] for _ in (mn, mx)]
                else:
                    mn, mx = [_.strftime("%Y-%m-%dT%H:%M:%S") for _ in (mn, mx)]
            else:
                mn, mx = [float(_) for _ in (mn, mx)]

            coords[name] = {"id": name, "min": mn, "max": mx, "length": len(data)}

        if coord_type == "time":
            if type(data[0]) == np.datetime64:
                coords[name]["calendar"] = "standard"
            else:
                coords[name]["calendar"] = data[0].calendar

        coords[name].update(coord.attrs)

    return coords


def _copy_dict_for_json(dct):
    d = {}

    for key, value in dct.items():

        if isinstance(value, np.floating):
            value = float(value)
        elif isinstance(value, np.integer):
            value = int(value)
        elif isinstance(value, np.ndarray):
            value = value.tolist()

        d[key] = value

    return d


def get_variable_metadata(da):
    d = _copy_dict_for_json(da.attrs)
    d["var_id"] = da.name

    # Encode _FillValue as string because representation may be strange

    d["_FillValue"] = str(da.encoding.get("_FillValue", "NOT_DEFINED"))

    return d


def get_global_attrs(ds, expected_attrs=None):
    if expected_attrs:
        LOGGER.info(f"Not testing expected attrs yet")

    d = _copy_dict_for_json(ds.attrs)
    return d


def get_data_info(da, mode):

    if mode == "full":

        mx = float(da.max())
        mn = float(da.min())

    else:
        mx = None
        mn = None

    return {
        "min": mn,
        "max": mx,
        "shape": da.shape,
        "rank": len(da.shape),
        "dim_names": da.dims,
    }


def get_scan_metadata(mode, location):
    return {
        "mode": mode,
        "last_scanned": datetime.now().isoformat(),
        "location": location,
    }


class CharacterExtractor(object):
    def __init__(self, files, location, var_id, mode, expected_attrs=None):
        """
        Open files as an Xarray MultiFile Dataset and extract character as a dictionary.
        Takes a dataset and extracts characteristics from it.

        :param files: List of data files.
        :param var_id: (string) The variable chosen as an argument at the command line.
        """
        self._files = files
        self._var_id = var_id
        self._mode = mode
        self._location = location
        self._expected_attrs = expected_attrs
        self._extract()

    def _extract(self):
        ds = xr.open_mfdataset(self._files, use_cftime=True, combine="by_coords")
        LOGGER.info(f"NEED TO CHECK NUMBER OF VARS/DOMAINS RETURNED HERE")
        LOGGER.info(f"DOES NOT CHECK YET WHETHER WE MIGHT GET 2 DOMAINS/VARIABLES BACK FROM MULTI-FILE OPEN"
        )
        # Get content by variable
        da = ds[self._var_id]
        self.character = {
            "scan_metadata": get_scan_metadata(self._mode, self._location),
            "variable": get_variable_metadata(da),
            "coordinates": get_coords(da),
            "global_attrs": get_global_attrs(ds, self._expected_attrs),
            "data": get_data_info(da, self._mode),
        }


def extract_character(files, location, var_id, mode="full", expected_attrs=None):
    ce = CharacterExtractor(
        files, location, var_id, mode, expected_attrs=expected_attrs
    )
    return ce.character
