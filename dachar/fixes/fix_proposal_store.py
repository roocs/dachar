from copy import deepcopy

from dachar.utils.common import now_string
from dachar.utils.json_store import _BaseJsonStore


class FixProposalStore(_BaseJsonStore):
    """
    TODO:
    Manage workflows:

    1. Propose an existing fix but with different operands
     - just overwrite
    2. Propose a fix that already exists (i.e. a duplicate proposal), with different state
     - change state
    3. Propose a fix that already exists, with same state
     - ignore
    """

    """
    structure of record
        {'dataset_id': 'ds.1.1.1.1.1.1',
         'fixes': [{'fix': {'fix_id': 'fix_id',
                            'title': 'title',
                            'description': 'description',
                            'category': 'category',
                            'reference_implementation': 'ref_implementation',
                            'operands': 'operands'},
                    'history': [],
                    'reason': '',
                    'status': 'proposed',
                    'timestamp': '2020-04-29T14:41:52'}]}
                    
                    
    Are title, description, category, ref_implementation needed here?                
    Should ncml be in fix?
    """


    store_name = 'Fix Proposal Store'
    config = {'store_type': 'local',
              'local.base_dir': '/tmp/fix-proposal-store',
              'local.dir_grouping_level': 4}
    id_mappers = {'*': '__ALL__'}
    required_fields = ['dataset_id', 'fixes']
    search_defaults = []

    def _get_fix_container(self, fix, status, reason=''):
        return {'fix': fix,
                'status': status,
                'timestamp': now_string(),
                'reason': reason,
                'history': []}

    def _update_fix_container(self, container, fix, status, reason=''):
        history = deepcopy(container['history'])

        # Insert most recent change into first position in history
        history.insert(0, {'status': container['status'],
                           'timestamp': container['timestamp'],
                           'reason': container['reason']})

        to_update = {'fix': fix, 'status': status, 'reason': reason}
        container['history'] = history

        for key, value in to_update.items():
            container[key] = value

    def _update_or_add_fix(self, fix_id, content, fix, status, reason=''):
        # Go through list of fixes, if fix_id exists in the list, add to that item
        for this_fix in content['fixes']:
            if this_fix['fix']['fix_id'] == fix_id:
                self._update_fix_container(this_fix, fix, status, reason=reason)
                break
        else:
            fix_container = self._get_fix_container(fix, status, reason=reason)
            content['fixes'].append(fix_container)

    def propose(self, ds_id, fix):
        self._action_fix(ds_id, fix, 'proposed')

    def publish(self, ds_id, fix):
        self._action_fix(ds_id, fix, 'published')

    def reject(self, ds_id, fix, reason):
        self._action_fix(ds_id, fix, 'rejected', reason=reason)

    def withdraw(self, ds_id, fix, reason):
        self._action_fix(ds_id, fix, 'withdrawn', reason=reason)

    def _action_fix(self, ds_id, fix, status, reason=''):
        fix_id = fix['fix_id']

        if self.exists(ds_id):
            content = self.get(ds_id)
        else:
            content = {'dataset_id': ds_id,
                       'fixes': []}

        self._update_or_add_fix(fix_id, content, fix, status=status, reason=reason)
        self.put(ds_id, content, force=True)

    # def get_proposed_fixes(self, ds_id):
    #     # go through fixes and return if status is proposed
    #     if self.exists(ds_id):
    #         content = self.get(ds_id)
    #         for this_fix in content['fixes']:
    #             if this_fix['status'] == 'proposed':
    #                 return this_fix['fix']

    def get_proposed_fixes(self):
        # go through fixes and return if status is proposed
        proposed_fixes = []

        for ds_id, content in self.get_all():
            if self.exists(ds_id):
                content = self.get(ds_id)
                for this_fix in content['fixes']:
                    if this_fix['status'] == 'proposed':
                        proposed_fixes.append(content)
                        # proposed_fixes.append(this_fix['fix'])

        return proposed_fixes



