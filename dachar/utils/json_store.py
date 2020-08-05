import json
import hashlib
import os


from .common import nested_lookup
from elasticsearch import Elasticsearch, helpers
from ceda_elasticsearch_tools.elasticsearch import CEDAElasticsearchClient


class _BaseJsonStore(object):
    store_name = "_BASE"
    config = {}
    id_mappers = {"*": "__ALL__"}
    required_fields = []

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
        }

        for key, dtype in required.items():
            if not hasattr(cls, key) or not type(getattr(cls, key)) is dtype:
                raise Exception(f"Invalid store definition: check class attr: {key}")

    def get(self, id):
        raise NotImplementedError

    def exists(self, id):
        raise NotImplementedError

    def delete(self, id):
        raise NotImplementedError

    def put(self, id, content, force=False):
        if self.exists(id) and not force:
            raise FileExistsError(
                f'Record already exists: {id}. Use "force=True" to overwrite.'
            )

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

    def _map(self, x, reverse=False):
        # Applies name mappers to/from ID/path
        mapper = self.id_mappers

        if reverse:
            mapper = {v: k for k, v in self.id_mappers.items()}

        for find_s, replace_s in mapper.items():
            x = x.replace(find_s, replace_s)

        return x

    def _save(self, id, content):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def get_all_ids(self):
        raise NotImplementedError

    def search(self, term, exact=False, match_ids=True, fields=None):
        raise NotImplementedError

    def _lookup(self, key_path, item, must_exist=False):
        return nested_lookup(key_path, item, must_exist=must_exist)


class _LocalBaseJsonStore(_BaseJsonStore):

    config = {
        "store_type": "local",
        "local.base_dir": "/tmp/json-store",
        "local.dir_grouping_level": 4,
        "index": "base",
    }

    def get(self, id):
        if not self.exists(id):
            return None

        json_path = self._id_to_path(id)

        with open(json_path) as reader:
            return json.load(reader)

    def exists(self, id):
        json_path = self._id_to_path(id)
        return os.path.exists(json_path)

    def delete(self, id):

        if not self.exists(id):
            raise Exception(f"Record with ID {id} does not exist")

        json_path = self._id_to_path(id)
        os.remove(json_path)
        dr = os.path.dirname(json_path)

        while len(dr) > len(self.config["local.base_dir"]):
            if not os.listdir(dr):
                os.rmdir(dr)

            dr = os.path.dirname(dr)

    def _save(self, id, content):
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
        for id in self.get_all_ids():
            yield id, self.get(id)

    def search(self, term, exact=False, match_ids=True, fields=None):
        results = []

        for _id, record in self.get_all():
            if (match_ids and self._match_id(term, _id, exact=exact)) or self._match(
                record, term, exact=exact, fields=fields
            ):
                results.append(record)

        return results



    def _id_to_path(self, id):
        # Define a "grouped" ds_id that splits facets across directories and then groups
        # the final set into a file path, based on config.DIR_GROUPING_LEVEL value
        gl = self.config["local.dir_grouping_level"]
        parts = id.split(".")

        if len(parts) <= gl:
            raise KeyError(
                f"Identifier name cannot be safely translated to file path: {id}"
            )

        grouped_id = "/".join(parts[:-gl]) + "/" + ".".join(parts[-gl:])
        fpath = os.path.join(self.config["local.base_dir"], grouped_id + ".json")

        return self._map(fpath)

    def _path_to_id(self, fpath):
        # Opposite of self._id_to_path()
        s = fpath.replace(self.config["local.base_dir"], "").strip("/")
        s = os.path.splitext(s)[0]

        s = s.replace("/", ".")
        return self._map(s, reverse=True)

    def get_all_ids(self):
        bdir = self.config["local.base_dir"]

        for dr, _, files in os.walk(bdir):
            for fpath in files:
                yield self._path_to_id(os.path.join(dr, fpath))

    def _match(self, record, term, exact=False, fields=None):
        search_fields = set()
        term = str(term).lower()

        if fields:
            search_fields = set(fields)

        # If no search fields defined - then search whole record as a string
        use_entire_record = "__USE_ENTIRE_RECORD__"
        if not search_fields:
            search_fields = [use_entire_record]

        for field in search_fields:

            if field == use_entire_record:
                found = record
            else:
                found = self._lookup(field, record)

            found = str(found).lower()
            if term == found or (not exact and term in found):
                return True

        return False

    def _match_id(self, term, id, exact=False):
        term = str(term).lower()
        id = str(id).lower()

        if term == id or (not exact and term in id):
            return True

        return False


class _ElasticSearchBaseJsonStore(_BaseJsonStore):
    config = {"store_type": "elasticsearch",
              "index": "",
              "api_token": None,
              "id_type": "id"}

    def __init__(self):
        super().__init__()
        api_token = self.config.get("api_token")
        if api_token is not None:
            self.es = CEDAElasticsearchClient(headers={
            "x-api-key": api_token
            })
        else:
            self.es = Elasticsearch("elasticsearch.ceda.ac.uk")

    def _convert_id(self, id):
        m = hashlib.md5()
        m.update(id.encode("utf-8"))
        return m.hexdigest()

    def get(self, id):
        if not self.exists(id):
            return None

        id = self._convert_id(id)
        res = self.es.get(index=self.config.get("index"), id=id)
        return res["_source"]

    def exists(self, id):
        id = self._convert_id(id)
        res = self.es.exists(index=self.config.get("index"), id=id)
        return res

    def delete(self, id):
        if not self.exists(id):
            raise Exception(f"Record with ID {id} does not exist")

        id = self._convert_id(id)
        self.es.delete(index=self.config.get("index"), id=id)

    def _save(self, id, content):
        drs_id = id
        id = self._convert_id(id)
        if "." in id:
            raise KeyError(
                f"Identifier name cannot be used as elasticsearch id as it contains .: {id} "
            )

        self.es.index(index=self.config.get("index"), body=content, id=id)

        self._map(drs_id, reverse=True)#
        self.es.update(index=self.config.get("index"),
                       id=id, body={"doc": {self.config.get("id_type"): drs_id}})

    def get_all_ids(self):
        # Generator to return all records
        results = helpers.scan(
            self.es, index=self.config.get("index"), query={"_source": [self.config.get("id_type")]}
        )
        for item in results:
            yield (item["_source"][self.config.get("id_type")])

    def get_all(self):
        # Generator to return all ids
        results = helpers.scan(
            self.es, index=self.config.get("index"), query={"query": {"match_all": {}}},
        )
        for item in results:
            yield (item["_source"])

    def _search_fields(self, fields, term, query_type):

        results = []

        query_body = {"query": {"bool": {"must": ""}}}

        keyword_fields = []
        for field in fields:
            keyword_fields.append(f"{field}.keyword")

        for field in fields + keyword_fields:
            match = {query_type: {field: term}}
            query_body["query"]["bool"]["must"] = match
            result = self.es.search(index=self.config.get("index"), body=query_body)
            if result["hits"]["hits"] is not None:
                for each in result["hits"]["hits"]:
                    results.append(each["_source"])

        # ensure there are no duplicates of the same result
        return dict((v[self.config.get("id_type")], v) for v in results).values()

    def _search_all(self, term):

        results = []

        query_body = {"query": {"query_string": {"query": ""}}}

        query_body["query"]["query_string"]["query"] = term
        result = self.es.search(index=self.config.get("index"), body=query_body)
        if result["hits"]["hits"] is not None:
            for each in result["hits"]["hits"]:
                results.append(each["_source"])

        # ensure there are no duplicates of the same result
        return dict((v[self.config.get("id_type")], v) for v in results).values()

    def _field_requirements(self, fields, term, query_type):

        if fields is not None:
            fields.append("ds_id")
            return self._search_fields(fields, term, query_type)
        else:
            return self._search_all(term)

    def search(
        self, term, exact=False, match_ids=True, fields=None
    ):

        if isinstance(term, float) or isinstance(term, int):
            exact = True
            print("[INFO]: Must search for exact value when the search term is a number,"
                  " Changing search to exact=True")

        if isinstance(term, str) and ' ' in term and exact is False:
            print("[INFO]: Ensure the case of your search term is correct as this type of "
                  "search is case sensitive. If you are not sure of the correct case change "
                  "your search term to a one word search or use exact=True.")

        if match_ids is True and exact is True:
            query_type = "term"
            return self._field_requirements(fields, term, query_type)

        elif match_ids is False and exact is True:
            query_type = "term"
            return self._field_requirements(fields, term, query_type)

        elif match_ids is False and exact is False:
            term = f'*{term.replace(" ","*")}*'
            query_type = "wildcard"
            return self._field_requirements(fields, term, query_type)

        elif match_ids is True and exact is False:
            term = f'*{term.replace(" ","*")}*'
            query_type = "wildcard"
            return self._field_requirements(fields, term, query_type)
