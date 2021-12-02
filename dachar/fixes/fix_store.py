from dachar.utils.json_store import _LocalBaseJsonStore, _ElasticSearchBaseJsonStore
from dachar import CONFIG


class BaseFixStore(object):

    store_name = "Fix Store"
    id_mappers = {"*": "__ALL__"}
    required_fields = ["dataset_id", "fixes"]

    def publish_fix(self, ds_id, fix_content):
        if self.exists(ds_id):
            content = self.get(ds_id)
            # Just in case: remove old fixes with same fix id
            self._remove_fix_from_list(fix_content["fix_id"], content["fixes"])
        else:
            content = {"dataset_id": ds_id, "fixes": []}

        content["fixes"].append(fix_content)
        self.put(ds_id, content, force=True)

    def withdraw_fix(self, ds_id, fix_id):
        if not self.exists(ds_id):
            raise Exception(f"No fixes exist for data set: {ds_id}")

        content = self.get(ds_id)
        self._remove_fix_from_list(fix_id, content["fixes"])

        if content["fixes"]:
            self.put(ds_id, content, force=True)
        else:
            self.delete(ds_id)

    def _remove_fix_from_list(self, fix_id, fixes_list):
        for fix in fixes_list:
            if fix["fix_id"] == fix_id:
                fixes_list.remove(fix)
                break


class LocalFixStore(_LocalBaseJsonStore, BaseFixStore):
    config = {
        "store_type": "local",
        "local.base_dir": CONFIG["dachar:store"].get("fix_store",
                          "/tmp/fix-store"),
        "local.dir_grouping_level": CONFIG["dachar:settings"].get(
                                           "dir_grouping_level", 4)

    }


class ElasticFixStore(_ElasticSearchBaseJsonStore, BaseFixStore):

    config = {
        "store_type": "elasticsearch",
        "index": CONFIG['elasticsearch']["fix_store"],
        "api_token": CONFIG['dachar:settings']['elastic_api_token'],
        "id_type": "dataset_id",
    }
