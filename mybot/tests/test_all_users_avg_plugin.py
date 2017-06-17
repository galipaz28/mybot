import unittest
import json
import time
from plugins.all_users_avg_plugin import AllUsersAvgJob
from tests.config import JSON_TESTS_PATH
INTERVAL = 2
CHANNEL = 'test_channel'


class TestUserAvgJob(unittest.TestCase):

    def setUp(self):
        self.job = AllUsersAvgJob(INTERVAL, CHANNEL, JSON_TESTS_PATH)
        self._setup_json_with_users_numbers()

    def _setup_json_with_users_numbers(self):
        with open(self.job._users_numbers_json_path, 'wb') as f:
            users_dict = {'test_user': {'sum': 21.0, 'counter': 3.0}}
            json.dump(users_dict, f)

    def test_new_messages_since_the_last_job_when_there_were_new_messages(self):
        self.assertTrue(self.job._check_if_there_were_new_numbers_since_last_time())

    def test_new_messages_since_the_last_job_when_there_were_not_new_messages(self):
        time.sleep(self.job.interval + 1)
        self.assertFalse(self.job._check_if_there_were_new_numbers_since_last_time())

    def test_get_all_users_avg(self):
        self.assertEqual(7.0, self.job._get_all_users_avg())
