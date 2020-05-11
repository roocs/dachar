from datetime import datetime

import numpy as np
import xarray as xr

# NOTE THESE ARE COMMON WITH clisops - need to merge!!!
def get_coord_by_attr(dset, attr, value):
    coords = dset.coords

    for coord in coords.values():
        if coord.attrs.get(attr, None) == value:
            return coord

    return None


def is_latitude(coord):
    return coord.attrs.get('standard_name') == 'latitude'


def is_longitude(coord):
    return coord.attrs.get('standard_name') == 'longitude'


def is_level(coord):
    raise NotImplementedError()


def is_time(coord):
    return coord.attrs.get('standard_name') == 'time'


def get_coord_type(coord):
    for ctype in ('time', 'latitude', 'longitude'):
        if coord.attrs.get('standard_name', None) == ctype:
            return ctype


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
    print(f'[DEBUG] Found coords: {str(da.coords.keys())}')
    print(f'[WARN] NOT CAPTURING scalar COORDS BOUND BY coorindates attr yet!!!')

    for coord_id in da.coords.dims:
        coord = da.coords[coord_id]

        coord_type = get_coord_type(coord)
        name = coord_type or coord.name
        data = coord.values

        mn, mx = data.min(), data.max()

        if coord_type == 'time':
            if type(mn) == np.datetime64:
                mn, mx = [str(_).split('.')[0] for _ in (mn, mx)]
            else:
                mn, mx = [_.strftime('%Y-%m-%dT%H:%M:%S') for _ in (mn, mx)]
        else:
            mn, mx = [float(_) for _ in (mn, mx)]

        coords[name] = {
            'id': name,
            'min': mn,
            'max': mx,
            'length': len(data)
        }

        if coord_type == 'time':
            if type(data[0]) == np.datetime64:
                coords[name]['calendar'] = 'standard'
            else:
                coords[name]['calendar'] = data[0].calendar

        coords[name].update(coord.attrs)

    return coords


def _copy_dict_for_json(dct):

    d = {}

    for key, value in dct.items():

        if isinstance(value, np.floating):
            value = float(value)
        elif isinstance(value, np.integer):
            value = int(value)

        d[key] = value

    return d


def get_variable_metadata(da):
    d = _copy_dict_for_json(da.attrs)
    d['var_id'] = da.name

    # Encode _FillValue as string because representation may be strange
    d['_FillValue'] = str(da.encoding.get('_FillValue', 'NOT_DEFINED'))
    return d


def get_global_attrs(ds, expected_attrs=None):
    if expected_attrs:
        print('[WARN] Not testing expected attrs yet')

    d = _copy_dict_for_json(ds.attrs)
    return d


def get_data_info(da, mode):
    if mode == 'full':
        data = da.values
        mx = float(data.max())
        mn = float(data.min())

    else:
        mx = None
        mn = None

    return {
        'min': mn,
        'max': mx,
        'shape': [da[f'{coord}'].size for coord in da.coords.keys()],
        'rank': len(da.shape),
        'coord_names': [_ for _ in da.coords.keys()]
    }


def get_scan_metadata(mode, location):

    return {
        'mode': mode,
        'last_scanned': datetime.now().isoformat(),
        'location': location,
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
        ds = xr.open_mfdataset(self._files, use_cftime=True, combine='by_coords')
        print('[WARN] NEED TO CHECK NUMBER OF VARS/DOMAINS RETURNED HERE')
        print('[WARN] DOES NOT CHECK YET WHETHER WE MIGHT GET 2 DOMAINS/VARIABLES BACK FROM MULTI-FILE OPEN')
        # Get content by variable
        da = ds[self._var_id]

        self.character = {
            "scan_metadata": get_scan_metadata(self._mode, self._location),
            "variable": get_variable_metadata(da),
            "coordinates": get_coords(da),
            "global_attrs": get_global_attrs(ds, self._expected_attrs),
            "data": get_data_info(da, self._mode)
        }


def extract_character(files, location, var_id, mode='full', expected_attrs=None):
    ce = CharacterExtractor(files, location, var_id, mode, expected_attrs=expected_attrs)
    return ce.character
