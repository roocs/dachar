from dachar.utils.common import UNDEFINED
from dachar import __version__ as version


class FixDetails(object):
    def __init__(
        self,
        ds_id,
        fix_id,
        title,
        description,
        category,
        ref_implementation,
        process_type,
        operands,
        source,
    ):
        self.record = {
            "dataset_id": {"ds_id": ds_id},
            "fix": {
                "fix_id": fix_id,
                "title": title,
                "description": description,
                "category": category,
                "reference_implementation": ref_implementation,
                "process_type": process_type,
                "operands": operands,
                "source": source,
            },
        }

    @property
    def dict(self):
        return self.record


class _BaseDatasetFix(object):

    fix_id = UNDEFINED
    title = UNDEFINED
    description = UNDEFINED

    category = UNDEFINED
    required_operands = UNDEFINED
    ref_implementation = UNDEFINED
    process_type = UNDEFINED

    ncml_template = """E.g. ...
    <variable name="temperature">
      <logicalReduce dimNames="latitude longitude" />
    </variable>
        """

    def __init__(self, ds_id, source=f"dachar version {version}", **operands):
        self.ds_id = ds_id
        self.source = source
        self.operands = operands
        self._validate()

    def _validate(self):
        missing_operands = set(self.required_operands).difference(set(self.operands))
        if missing_operands:
            raise KeyError(
                f"Required keyword argument(s) not provided: {missing_operands}"
            )

        invalid_operands = set(self.operands).difference(set(self.required_operands))
        if invalid_operands:
            raise KeyError(f"Invalid keyword arguments received: {invalid_operands}")

    def __repr__(self):
        return f"""<Fix: {self.fix_id} (category: {self.category})>

{self.description}

Operands: {self.operands}
"""

    def to_ncml(self):
        return self.ncml_template.format(**self.operands)

    def to_dict(self):
        d = FixDetails(
            self.ds_id,
            self.fix_id,
            self.title,
            self.description,
            self.category,
            self.ref_implementation,
            self.process_type,
            self.operands,
            self.source,
        )

        return d.dict
