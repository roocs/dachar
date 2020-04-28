from ._base_check import _BaseCheck
from dachar.fixes.fix_api import get_fix


class RankCheck(_BaseCheck):

    characteristics = ['data.coord_names', 'data.shape']
    associated_fix = 'SqueezeDimensionsFix'


    def _deduce_fix(self, atypical_content, typical_content):
        x = atypical_content['data.coord_names']

        fix_cls = get_fix(self.associated_fix)
        operands = {'a': 1, 'b': 2}

        fix = fix_cls(ds_id, **operands)
        d = fix.to_dict()
        return d



