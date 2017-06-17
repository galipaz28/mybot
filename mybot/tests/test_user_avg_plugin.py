import unittest
from collections import defaultdict
import json
from plugins.user_avg_plugin import UserAvgPlugin
from tests.config import JSON_TESTS_PATH


class TestUserAvgPlugin(unittest.TestCase):

    def _setup_plugin_without_data_history(self):
        self.plugin = UserAvgPlugin(clean_data_history=True, users_numbers_json_path=JSON_TESTS_PATH)

    def _setup_plugin_with_data_history(self):
        self.plugin = UserAvgPlugin(clean_data_history=False, users_numbers_json_path=JSON_TESTS_PATH)

    def _setup_test_user_to_plugin(self):
        self.plugin._users_numbers['test_user']['sum'] = 20.0
        self.plugin._users_numbers['test_user']['counter'] = 4.0

    def test_users_numbers_dict_in_new_without_data_history_plugin(self):
        self._setup_plugin_without_data_history()
        self.assertTrue(isinstance(self.plugin._users_numbers, defaultdict))
        self.assertEqual(0, len(self.plugin._users_numbers))

    def test_users_numbers_dict_in_new_with_data_history_plugin(self):
        self._setup_plugin_with_data_history()
        self.assertTrue(isinstance(self.plugin._users_numbers, defaultdict))
        with open(JSON_TESTS_PATH, 'rb') as f:
            users_dict = json.load(f)
        self.assertEqual(users_dict, dict(self.plugin._users_numbers))

    def test_add_data_to_user_function_on_the_first_time(self):
        self._setup_plugin_without_data_history()
        self.plugin._add_data_to_user('test_user2', 5)
        self.assertEqual({'sum': 5.0, 'counter': 1.0}, self.plugin._users_numbers['test_user2'])

    def test_add_data_to_user_function_on_the_second_time(self):
        self._setup_plugin_without_data_history()
        self.plugin._add_data_to_user('test_user2', 8)
        self.plugin._add_data_to_user('test_user2', 10)
        self.assertEqual({'sum': 18.0, 'counter': 2.0}, self.plugin._users_numbers['test_user2'])

    def test_get_user_avg_function_on_existing_user(self):
        self._setup_plugin_without_data_history()
        self._setup_test_user_to_plugin()
        self.assertEqual(5.0, self.plugin._get_user_avg('test_user'))

    def test_get_user_avg_function_on_non_existing_user(self):
        self._setup_plugin_without_data_history()
        with self.assertRaises(ZeroDivisionError):
            self.plugin._get_user_avg('user_name')

    def test_check_message_is_number_on_int_number(self):
        self._setup_plugin_without_data_history()
        self.assertTrue(self.plugin._check_message_is_number(7))

    def test_check_message_is_number_on_float_number(self):
        self._setup_plugin_without_data_history()
        self.assertTrue(self.plugin._check_message_is_number(7.5))

    def test_check_message_is_number_on_string_number(self):
        self._setup_plugin_without_data_history()
        self.assertTrue(self.plugin._check_message_is_number('7'))

    def test_check_message_is_number_on_string(self):
        self._setup_plugin_without_data_history()
        self.assertFalse(self.plugin._check_message_is_number('hi'))

    def test_get_user_name_from_user_id(self):
        self._setup_plugin_without_data_history()
        self.plugin._user_id_to_user_name['test_user_id'] = 'test_user_name'
        return self.assertEqual('test_user_name', self.plugin._get_user_name_from_user_id('test_user_id'))
