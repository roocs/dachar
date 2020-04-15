from dachar.utils.json_store import _BaseJsonStore


class FixStore(_BaseJsonStore):

    store_name = 'Fix Store'
    config = {'store_type': 'local',
              'local.base_dir': '/tmp/fix-store',
              'local.dir_grouping_level': 4}
    id_mappers = {'*': '__ALL__'}
    required_fields = ['dataset_id', 'fixes', 'history',
                       'fixes.fix_id', 'fixes.operands',
                       'fixes.ncml']
    search_defaults = []


fix_store = FixStore()

