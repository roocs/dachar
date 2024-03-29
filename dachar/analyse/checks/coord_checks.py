import pprint
from collections import Counter
from collections import namedtuple
from itertools import chain

from scipy.stats import mode

from dachar import __version__ as version
from dachar.analyse.checks._base_check import _BaseCheck
from dachar.fixes.fix_api import get_fix
from dachar.utils import nested_lookup
from dachar.utils.common import coord_mappings
from dachar.utils.common import get_extra_items_in_larger_sequence


class RankCheck(_BaseCheck):
    characteristics = ["data.dim_names", "data.shape"]
    associated_fix = "SqueezeDimensionsFix"

    source = {
        "name": "dachar",
        "version": f"{version}",
        "comment": "",
        "url": "https://github.com/roocs/dachar/blob/master/dachar/fixes/coord_fixes.py#L8",
    }

    def deduce_fix(self, ds_id, atypical_content, typical_content):
        dicts = []

        atypical = atypical_content["data.dim_names"]
        typical = typical_content["data.dim_names"]

        # length of atypical should be longer if extra coord
        # Will this always be the case?
        if len(atypical) <= len(typical):
            return None

        extra_coords = get_extra_items_in_larger_sequence(typical, atypical)

        if extra_coords:

            if len(extra_coords) > 0:

                fix_cls = get_fix(self.associated_fix)

                for coord in extra_coords:
                    index = atypical.index(coord)
                    if atypical_content["data.shape"][index] != 1:
                        extra_coords.remove(coord)

                    operands = {"dims": extra_coords}

                    fix = fix_cls(ds_id, source=self.source, **operands)
                    d = fix.to_dict()
                    dicts.append(d)
                return dicts

        # fix isn't suitable - no extra coords
        else:
            return None


# TODO: Need to change this so that characteristic compared is coord_type
#   But characteristic used to create new variable is id


class MissingCoordCheck(_BaseCheck):
    characteristics = ["coordinates.*.id"]
    associated_fix = "AddScalarCoordFix"

    source = {
        "name": "dachar",
        "version": f"{version}",
        "comment": "",
        "url": "https://github.com/roocs/dachar/blob/master/dachar/fixes/coord_fixes.py#L44",
    }

    def deduce_fix(self, ds_id, atypical_content, typical_content):
        dicts = []

        atypical = atypical_content["coordinates.*.id"]
        typical = typical_content["coordinates.*.id"]

        # length of atypical should be shorter if missing coord
        # Will this always be the case?
        if len(atypical) >= len(typical):
            return None

        # # use mappings to get equivalent coords
        # for coord in atypical:
        #     if coord not in typical:
        #         equivalent_coord = coord_mappings[coord]
        #         atypical = [equivalent_coord if i == coord else i for i in atypical]

        missing_coords = get_extra_items_in_larger_sequence(atypical, typical)

        if missing_coords:

            if len(missing_coords) > 0:
                fix_cls = get_fix(self.associated_fix)

                for coord in missing_coords:

                    typical_coord_attrs = []
                    typical_ds_ids = self.sample.copy()
                    typical_ds_ids.remove(ds_id[0])

                    for ds in typical_ds_ids:

                        coord_attrs = nested_lookup(
                            f"coordinates.{coord}", self._cache[ds], must_exist=True
                        )
                        coord_attrs = namedtuple("coord_attrs", coord_attrs.keys())(
                            **coord_attrs
                        )

                        typical_coord_attrs.append(coord_attrs)

                    frequency = Counter(d for d in typical_coord_attrs)
                    typical_coord = frequency.most_common(1)[0][0]
                    typical_length = typical_coord.length

                    # check missing coord is scalar
                    if typical_length == 1:
                        operands = {}

                        operand_dict = dict(typical_coord._asdict())
                        for k in ["dtype", "value", "var_id", "encoding"]:
                            v = operand_dict.pop(k)

                            operands[k] = v

                        operands["attrs"] = operand_dict

                        fix = fix_cls(ds_id, source=self.source, **operands)
                        d = fix.to_dict()

                    # coordinate isn't scalar - fix isn't suitable
                    else:
                        d = None

                    dicts.append(d)

            return dicts

        # fix isn't suitable - no missing coords
        else:
            return None
