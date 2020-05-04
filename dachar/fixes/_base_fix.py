
from dachar.utils.common import UNDEFINED


class FixDetails(object):
    """
    Structure of a fix
    """
    fix_template = {
        'fix_id': 'fix_id',
        'title': 'title',
        'description': 'description',
        'category': 'category',
        'reference_implementation': 'ref_implementation',
        'operands': 'operands'
    }


class _BaseDatasetFix(FixDetails):

    fix_id = UNDEFINED
    title = UNDEFINED
    description = UNDEFINED

    category = UNDEFINED
    required_operands = UNDEFINED
    ref_implementation = UNDEFINED

    ncml_template = """E.g. ...
    <variable name="temperature">
      <logicalReduce dimNames="latitude longitude" />
    </variable>
        """

    template = {'dataset_id': 'ds_id',
                'fix': FixDetails.fix_template}

    def __init__(self, ds_id, **operands):
        self.ds_id = ds_id
        self.operands = operands
        self._validate()

    def _validate(self):
        missing_operands = set(self.required_operands).difference(set(self.operands))
        if missing_operands:
            raise KeyError(f'Required keyword argument(s) not provided: {missing_operands}')

        invalid_operands = set(self.operands).difference(set(self.required_operands))
        if invalid_operands:
            raise KeyError(f'Invalid keyword arguments received: {invalid_operands}')

    def __repr__(self):
        return f"""<Fix: {self.fix_id} (category: {self.category})>

{self.description}

Operands: {self.operands}
"""

    def to_ncml(self):
        return self.ncml_template.format(**self.operands)

    def to_dict(self):
        d = {}

        d['dataset_id'] = getattr(self, 'ds_id')
        for k, getter in self.template['fix'].items():
            d[k] = getattr(self, getter)

        return d
