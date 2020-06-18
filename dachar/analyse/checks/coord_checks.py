from dachar.analyse.checks._base_check import _BaseCheck
from dachar.fixes.fix_api import get_fix
from dachar.utils.common import get_extra_items_in_larger_sequence
from dachar.utils import options
from dachar.utils import nested_lookup
from scipy.stats import mode
from collections import Counter, namedtuple
from itertools import chain
import pprint


class RankCheck(_BaseCheck):
    characteristics = ['data.dim_names', 'data.shape']
    associated_fix = 'SqueezeDimensionsFix'

    def deduce_fix(self, ds_id, atypical_content, typical_content):

        atypical = atypical_content['data.dim_names']
        typical = typical_content['data.dim_names']
        if len(atypical) > len(typical):
            extra_coords = get_extra_items_in_larger_sequence(typical, atypical)
        else:
            extra_coords = get_extra_items_in_larger_sequence(atypical, typical)

        if extra_coords:

            if len(extra_coords) > 0:

                fix_cls = get_fix(self.associated_fix)

                for coord in extra_coords:
                    index = atypical.index(coord)
                    if atypical_content['data.shape'][index] != 1:
                        extra_coords.remove(coord)

                operands = {'dims': extra_coords}

                fix = fix_cls(ds_id, **operands)
                d = fix.to_dict()
                return d

        # fix isn't suitable - no extra coords
        else:
            return None


class MissingCoordCheck(_BaseCheck):
    characteristics = ['coordinates.*.id']
    associated_fix = 'AddScalarCoordFix'

    def deduce_fix(self, ds_id, atypical_content, typical_content):
        atypical = atypical_content['coordinates.*.id']
        typical = typical_content['coordinates.*.id']

        for coord in atypical:
            if coord not in typical:
                equivalent_coord = options.coord_mappings[coord]
                atypical = [equivalent_coord if i == coord else i for i in atypical]

        if len(atypical) < len(typical):
            missing_coords = get_extra_items_in_larger_sequence(atypical, typical)

        else:
            missing_coords = None

        if missing_coords:

            if len(missing_coords) > 0:
                fix_cls = get_fix(self.associated_fix)

                for coord in missing_coords:
                    fix_characteristics = [f'coordinates.{coord}.length', f'coordinates.{coord}.length', f'coordinates.{coord}.length']



                    typical_lengths = []
                    typical_coord_attrs = []
                    typical_ds_ids = self.sample.copy()
                    typical_ds_ids.remove(ds_id[0])

                    for ds in typical_ds_ids:
                        
                        coord_attrs = nested_lookup(f'coordinates.{coord}', self._cache[ds], must_exist=True)
                        coord_attrs = namedtuple('coord_attrs', coord_attrs.keys())(**coord_attrs)

                        typical_coord_attrs.append(coord_attrs)

                    #     length = coord_attrs['length']
                    #     typical_lengths.append(length)
                    # typical_length = mode(typical_lengths)[0]
                    
                    frequency = Counter(d for d in typical_coord_attrs)
                    typical_coord = frequency.most_common(1)[0][0]
                    typical_length = typical_coord.length

                    # check missing coord is scalar
                    if typical_length == 1:
                        #operands = dict(typical_coord._asdict())
                        operands = {'dtype': typical_coord.dtype,
                                    'id': typical_coord.id,
                                    'length': typical_coord.length,
                                    'value': typical_coord.value,
                                    'attrs': ''}

                        fix = fix_cls(ds_id, **operands)
                        d = fix.to_dict()
                        return d

                    # coordinate isn't scalar - fix isn't suitable
                    else:
                        return None

        # fix isn't suitable - no missing coords
        else:
            return None