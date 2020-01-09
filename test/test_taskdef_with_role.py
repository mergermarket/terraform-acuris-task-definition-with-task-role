import json
import unittest

from subprocess import check_call, check_output


class TestTaskdefWithRole(unittest.TestCase):

    def setUp(self):
        check_call(['terraform', 'get', 'test/infra'])
        check_call(['terraform', 'init', 'test/infra'])

    def get_output_json(self):
        return json.loads(check_output([
            'terraform',
            'show',
            '-json',
            'plan.out'
        ]).decode('utf-8'))

    def get_resource_changes(self):
        output = self.get_output_json()
        return output.get('resource_changes')

    def assert_resource_changes_action(self, resource_changes, action, length):
        resource_changes_create = [
            rc for rc in resource_changes
            if rc.get('change').get('actions') == [action]
        ]
        assert len(resource_changes_create) == length

    def assert_resource_changes(self, testname, resource_changes):
        with open(f'test/files/{testname}.json', 'r') as f:
            data = json.load(f)

            assert data.get('resource_changes') == resource_changes

    def test_task_definition_is_created(self):
        # Given When
        check_call([
            'terraform',
            'plan',
            '-out=plan.out',
            '-no-color',
            '-target=module.taskdef_with_role',
            'test/infra'
        ])

        resource_changes = self.get_resource_changes()

        # Then
        assert len(resource_changes) == 5
        self.assert_resource_changes_action(resource_changes, 'create', 5)
        self.assert_resource_changes(
            'task_definition_is_created', resource_changes)

    def test_task_definition_passes_volume(self):
        # Given When
        check_call([
            'terraform',
            'plan',
            '-out=plan.out',
            '-no-color',
            '-var',
            'task_volume_param={name="data_volume", host_path="/mnt/data"}',
            '-target=module.taskdef_with_role',
            'test/infra'
        ])

        resource_changes = self.get_resource_changes()

        # Then
        assert len(resource_changes) == 5
        self.assert_resource_changes_action(resource_changes, 'create', 5)
        self.assert_resource_changes(
            'task_definition_passes_volume', resource_changes)

    def test_task_definition_is_created_when_long_family_name(self):
        # Given When
        check_call([
            'terraform',
            'plan',
            '-out=plan.out',
            '-no-color',
            '-var', 'family_param=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            '-target=module.taskdef_with_role',
            'test/infra'
        ])

        resource_changes = self.get_resource_changes()

        # Then
        assert len(resource_changes) == 5
        self.assert_resource_changes_action(resource_changes, 'create', 5)
        self.assert_resource_changes(
            'task_definition_is_created_when_long_family_name', resource_changes)

    def test_task_role_is_created_with_custom_assume_role_policy(self):
        # Given When
        check_call([
            'terraform',
            'plan',
            '-out=plan.out',
            '-no-color',
            '-target=module.taskdef_with_role_and_assume_role',
            'test/infra'
        ])

        resource_changes = self.get_resource_changes()

        # Then
        assert len(resource_changes) == 6
        self.assert_resource_changes_action(resource_changes, 'create', 5)
        self.assert_resource_changes(
            'task_role_is_created_with_custom_assume_role_policy', resource_changes)
