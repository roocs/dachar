import json
import os


class _BaseJsonStore(object):

    store_name = "_BASE"
    config = {
        "store_type": "local",
        "local.base_dir": "/tmp/json-store",
        "local.dir_grouping_level": 4,
    }
    id_mappers = {"*": "__all__"}
    required_fields = []
    search_defaults = []

    def __init__(self):
        self._verify_store()

    def _verify_store(self):
        # Checks all class attributes to make sure they are all valid
        cls = self.__class__

        required = {
            "store_name": str,
            "config": dict,
            "id_mappers": dict,
            "required_fields": list,
            "search_defaults": list,
        }

        for key, _type in required.items():
            if not hasattr(cls, key) or not isinstance(getattr(cls, key), _type):
                raise Exception(f"Invalid store definition: check class attr: {key}")

    def get(self, id):
        if not self.exists(id):
            return None

        stype = self.config.get("store_type")

        if stype == "local":
            return self._get_local(id)

    def _get_local(self, id):
        json_path = self._id_to_path(id)

        with open(json_path) as reader:
            return json.load(reader)

    def exists(self, id):
        stype = self.config.get("store_type")

        if stype == "local":
            return self._exists_local(id)

    def _exists_local(self, id):
        json_path = self._id_to_path(id)
        return os.path.exists(json_path)

    def delete(self, id):
        stype = self.config.get("store_type")

        if stype == "local":
            return self._delete_local(id)

    def _delete_local(self, id):
        if not self.exists(id):
            raise Exception(f"Record does not exist with ID: {id}")

        json_path = self._id_to_path(id)
        os.remove(json_path)
        dr = os.path.dirname(json_path)

        while len(dr) > len(self.config["local.base_dir"]):
            if not os.listdir(dr):
                os.rmdir(dr)

            dr = os.path.dirname(dr)

    def put(self, id, content):
        self._validate(content)
        self._save(id, content)

    def _validate(self, content):
        try:
            s = json.dumps(content)
            assert s.startswith("{") and s.endswith("}")
        except Exception as exc:
            raise ValueError("Cannot serialise content to valid JSON.")

        self._validate_fields(content)

    def _validate_fields(self, content):
        errors = []

        for key_path in self.required_fields:
            try:
                self._lookup(key_path, content, must_exist=True)
            except KeyError as exc:
                errors.append(str(exc))

        if errors:
            raise ValueError(f"Validation errors:\n{[err for err in errors]}")

    def _save(self, id, content):
        stype = self.config.get("store_type")

        if stype == "local":
            return self._save_local(id, content)

    def _save_local(self, id, content):
        json_path = self._id_to_path(id)

        dr = os.path.dirname(json_path)
        if not os.path.isdir(dr):
            os.makedirs(dr)

        try:
            with open(json_path, "w") as writer:
                json.dump(content, writer, indent=4, sort_keys=True)
        except Exception as exc:
            raise IOError(f"Cannot write content for: {id} to path {json_path}")

    def get_all(self):
        # Generator to return all records
        for id in self._get_all_ids():
            yield id, self.get(id)

    def search(
        self, term, exact=False, match_ids=False, fields=None, ignore_defaults=False
    ):
        results = []

        for _id, record in self.get_all():
            if (match_ids and self._match_id(term, _id, exact=exact)) or self._match(
                record,
                term,
                exact=exact,
                fields=fields,
                ignore_defaults=ignore_defaults,
            ):
                results.append(record)

        return results

    def _map(self, x, reverse=False):
        # Applies name mappers to/from ID/path
        mapper = self.id_mappers

        if reverse:
            mapper = {v: k for k, v in self.id_mappers.items()}

        for find_s, replace_s in mapper.items():
            x = x.replace(find_s, replace_s)

        return x

    def _id_to_path(self, id):
        # Define a "grouped" ds_id that splits facets across directories and then groups
        # the final set into a file path, based on config.DIR_GROUPING_LEVEL value
        gl = self.config["local.dir_grouping_level"]
        parts = id.split(".")

        grouped_id = "/".join(parts[:-gl]) + "/" + ".".join(parts[-gl:])
        fpath = os.path.join(self.config["local.base_dir"], grouped_id + ".json")
        return self._map(fpath)

    def _path_to_id(self, fpath):
        # Opposite of self._id_to_path()
        s = fpath.replace(self.config["local.base_dir"], "").strip("/")
        s = os.path.splitext(s)[0]

        s = s.replace("/", ".")
        return self._map(s, reverse=True)

    def _get_all_ids(self):
        stype = self.config["store_type"]

        if stype == "local":
            return self._get_all_ids_local()

    def _get_all_ids_local(self):
        bdir = self.config["local.base_dir"]

        for dr, _, files in os.walk(bdir):
            for fpath in files:
                yield self._path_to_id(os.path.join(dr, fpath))

    def _lookup(self, key_path, item, must_exist=False):
        not_found = "___NOT_FOUND__"

        for key in key_path.split("."):
            if type(item) == dict:
                item = item.get(key, not_found)
            else:
                item = not_found

            if item == not_found:
                if must_exist:
                    raise KeyError(f'Required content "{key}" not found.')
                return None

        return item

    def _match(self, record, term, exact=False, fields=None, ignore_defaults=False):
        search_fields = set()
        term = str(term).lower()

        if fields:
            search_fields = set(fields)
        if not ignore_defaults:
            search_fields.update(set(self.search_defaults))

        for field in search_fields:
            found = str(self._lookup(field, record)).lower()

            if term == found or (not exact and term in found):
                return True

        return False

    def _match_id(self, term, id, exact=False):
        term = str(term).lower()
        id = str(id).lower()

        if term == id or (not exact and term in id):
            return True

        return False
