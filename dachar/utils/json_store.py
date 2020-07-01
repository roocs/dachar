import json
<<<<<<< HEAD
import hashlib

from .common import nested_lookup
from elasticsearch import Elasticsearch, helpers
from ceda_elasticsearch_tools.elasticsearch import CEDAElasticsearchClient

es = CEDAElasticsearchClient(headers={'x-api-key': ''})

class _BaseJsonStore(object):

    store_name = '_BASE'
    config = {'store_type': 'local',
              'local.base_dir': '/tmp/json-store',
              'local.dir_grouping_level': 4,
              'index': 'base'}
    id_mappers = {'*': '__ALL__'}
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

        for key, dtype in required.items():
            if not hasattr(cls, key) or not type(getattr(cls, key)) is dtype:
                raise Exception(f'Invalid store definition: check class attr: {key}')
            
    def convert_id(self, id):
        m = hashlib.md5()
        m.update(id.encode('utf-8'))
        return m.hexdigest()


    def get(self, id):
        if not self.exists(id):
            return None

        stype = self.config.get("store_type")

        if stype == "local":
            return self._get_local(id)

        if stype == 'elasticsearch':
            return self._get_elasticsearch(id)

    def _get_local(self, id):
        json_path = self._id_to_path(id)

        with open(json_path) as reader:
            return json.load(reader)

    def _get_elasticsearch(self, id):
        id = self.convert_id(id)
        res = es.get(index=self.config.get('index'), id=id)
        return res['_source']

    def exists(self, id):
        stype = self.config.get("store_type")

        if stype == "local":
            return self._exists_local(id)

        if stype == 'elasticsearch':
            return self._exists_elasticsearch(id)

    def _exists_local(self, id):
        json_path = self._id_to_path(id)
        return os.path.exists(json_path)

    def _exists_elasticsearch(self, id):
        id = self.convert_id(id)
        res = es.exists(index=self.config.get('index'), id=id)
        return res

    def delete(self, id):

        if not self.exists(id):
            raise Exception(f'Record with ID {id} does not exist')

        stype = self.config.get('store_type')

        if stype == "local":
            return self._delete_local(id)

        if stype == 'elasticsearch':
            return self._delete_elasticsearch(id)


    def _delete_local(self, id):
        json_path = self._id_to_path(id)
        os.remove(json_path)
        dr = os.path.dirname(json_path)

        while len(dr) > len(self.config["local.base_dir"]):
            if not os.listdir(dr):
                os.rmdir(dr)

            dr = os.path.dirname(dr)

    def _delete_elasticsearch(self, id):
        id = self.convert_id(id)
        es.delete(index=self.config.get('index'), id=id)

    def put(self, id, content, force=False):
        if self.exists(id) and not force:
            raise FileExistsError(f'Record already exists: {id}. Use "force=True" to overwrite.')

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

        if stype == 'elasticsearch':
            return self._save_elasticsearch(id, content)

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

    def _save_elasticsearch(self, id, content):
        id = self.convert_id(id)
        if '.' in id:
            raise KeyError(f'Identifier name cannot be used as elasticsearch id as it contains .: {id} ')

        es.index(index=self.config.get('index'), body=content, id=id)

    def get_all(self):
        # Generator to return all records
        stype = self.config.get('store_type')

        if stype == 'local':
            for id in self._get_all_ids_local():
                yield id, self.get(id)

        if stype == 'elasticsearch':
            results = helpers.scan(es, query={"query": {"match_all": {}}},)
            for item in results:
                yield (item['_id'], item['_source'])

    def search(self, term, exact=False, match_ids=True, fields=None, ignore_defaults=False):
        stype = self.config.get('store_type')

        if stype == 'local':
            _search_local(self, term, exact, match_ids, fields, ignore_defaults)

        if stype == 'elasticsearch':
            _search_elasticsearch(self, term, exact, match_ids, fields, ignore_defaults)

    def _search_elasticsearch(self, term, exact, match_ids, fields, ignore_defaults): # come back to this
        results = []

        query_body = {
            "query": {
                "bool": {
                    "must": []
                }
            }
        }

        for field in fields:
            match = {
                        "match" : {
                            field : term
                        }
                    },
            query_body['query']['bool']['must'] = match
            results.append(es.search(index=self.config.get('index'), body=query_body))

    def _search_local(self, term, exact, match_ids, fields, ignore_defaults):
        results = []

        for _id, record in self.get_all():
            if (match_ids and self._match_id(term, _id, exact=exact)) or \
                    self._match(record, term, exact=exact, fields=fields, ignore_defaults=ignore_defaults):


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

        if len(parts) <= gl:
            raise KeyError(f'Identifier name cannot be safely translated to file path: {id}')

        grouped_id = '/'.join(parts[:-gl]) + '/' + '.'.join(parts[-gl:])
        fpath = os.path.join(self.config['local.base_dir'], grouped_id + '.json')

        return self._map(fpath)

    def _path_to_id(self, fpath):
        # Opposite of self._id_to_path()
        s = fpath.replace(self.config["local.base_dir"], "").strip("/")
        s = os.path.splitext(s)[0]

        s = s.replace("/", ".")
        return self._map(s, reverse=True)


    # def _get_all_ids(self):
    #     stype = self.config['store_type']
    #
    #     if stype == 'local':
    #         return self._get_all_ids_local()


    def _get_all_ids_local(self):
        bdir = self.config["local.base_dir"]

        for dr, _, files in os.walk(bdir):
            for fpath in files:
                yield self._path_to_id(os.path.join(dr, fpath))

    def _lookup(self, key_path, item, must_exist=False):
        return nested_lookup(key_path, item, must_exist=must_exist)


    def _match(self, record, term, exact=False, fields=None, ignore_defaults=False):
        search_fields = set()
        term = str(term).lower()

        if fields:
            search_fields = set(fields)
        if not ignore_defaults:
            search_fields.update(set(self.search_defaults))

        # If no search fields defined - then search whole record as a string
        use_entire_record = '__USE_ENTIRE_RECORD__'
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
