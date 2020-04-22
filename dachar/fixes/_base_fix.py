import datetime


UNDEFINED = 'UNDEFINED'
ALLOWED_FIX_STATUSES = 'unset', 'suggested', 'rejected', 'accepted'


class _BaseDatasetFix(object):

    fix_id = UNDEFINED
    title = UNDEFINED
    description = UNDEFINED

    category = UNDEFINED
    required_kwargs = UNDEFINED
    ref_implementation = UNDEFINED

    status = UNDEFINED

    ncml_template = """E.g. ...
    <variable name="temperature">
      <logicalReduce dimNames="latitude longitude" />
    </variable>
        """

    template = {
      "fix_id": "{self.fix_id}",
      "category": "{self.category}",
      "kwargs": "{kwargs}"
    }


    def __init__(self, ds_id, **kwargs):
        self.ds_id = ds_id
        self.kwargs = kwargs
        self._validate()

        # TODO: WHAT IS THE PURPOSE OF LOAD!!!!???
        self._load()

    def _validate(self):
        missing_kwargs = set(self.required_kwargs).difference(set(self.kwargs))
        if missing_kwargs:
            raise KeyError(f'Required keyword argument(s) not provided: {missing_kwargs}')

        invalid_kwargs = set(self.kwargs).difference(set(self.required_kwargs))
        if invalid_kwargs:
            raise KeyError(f'Invalid keyword arguments received: {invalid_kwargs}')

    def _load(self):

        self.update('unset')

    def __repr__(self):
        return f"""<Fix: {self.fix_id} (category: {self.category})>

{self.description}

Keyword arguments: {self.kwargs}
"""

    def to_ncml(self):
        return self.ncml_template.format(**self.kwargs)

    def to_json(self):
        return self.template.format(**self.kwargs)

    def update(self, status):
        self.status = status

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value not in ALLOWED_FIX_STATUSES:
            raise ValueError(f'Invalid status: must be set to one of: {ALLOWED_FIX_STATUSES}')

        self.__status = value
        self.__last_updated = datetime.datetime.now()

    @property
    def last_updated(self):
        return self.__last_updated

