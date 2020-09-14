import datetime
import json
import os

import SETTINGS
from lib import utils
from dachar import logging, CONFIG

LOGGER = logging.getLogger(__file__)


example_fixes = {
    "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga": {
        "pre_processor": {
            "func": "daops.pre_processors.do_nothing",
            "args": None,
            "kwargs": None,
        },
        "post_processor": {
            "func": "daops.post_processors.squeeze_dims",
            "args": [1],
            "kwargs": None,
        },
    }
}


def write_fixes():

    ds_ids = ["cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"]

    for ds_id in ds_ids:

        grouped_ds_id = utils.get_grouped_ds_id(ds_id)
        json_path = CONFIG["dachar:output_paths"]["fix_path"].format(**vars())

        dr = os.path.dirname(json_path)
        if not os.path.isdir(dr):
            os.makedirs(dr)

        content = example_fixes

        with open(json_path, "w") as writer:
            json.dump(content, writer, indent=4, sort_keys=True)

        LOGGER.info(f"Wrote: {json_path}")


class _BaseFix(object):

    FIX_NAME = "UNDEFINED"
    CATEGORY = "UNDEFINED"
    DESCRIPTION = "UNDEFINED"

    ALLOWED_STATUSES = "unset", "suggested", "rejected", "accepted"

    NCML_TEMPLATE = """E.g. ...
<variable name="temperature">
  <logicalReduce dimNames="latitude longitude" />
</variable>
    """
    JSON_TEMPLATE = """{{
  "fix_name": "{self.FIX_NAME}",
  "category": "{self.CATEGORY}",
  "args": "{args}",
  "kwargs": "{kwargs}"
}}"""

    def __init__(self):
        self._load()

    def _load(self):

        self.update("unset")

    def __repr__(self):
        return f"""<Fix: {self.FIX_NAME} (category: {self.CATEGORY})>

{self.description}

Arguments: {self.args}
Keyword arguments: {self.kwargs}
"""

    def to_ncml(self):
        return self.NCML_TEMPLATE.format(**locals(), **globals())

    def to_json(self):
        return self.JSON_TEMPLATE.format(**locals(), **globals())

    def update(self, status):
        self.status = status

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value not in self.ALLOWED_STATUSES:
            raise ValueError(
                f"Invalid status: must be set to one of: {self.ALLOWED_STATUSES}"
            )

        self.__status = value
        self.__last_updated = datetime.datetime.now()

    @property
    def last_updated(self):
        return self.__last_updated


def main():

    write_fixes()


if __name__ == "__main__":

    main()
