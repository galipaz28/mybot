import json
import os
import time

from rtmbot.core import Plugin, Job

from config import USERS_AVG_JSON_PATH
from utils import calculate_avg_of_all_users_numbers


JOB_INTERVAL = 60
CHANNEL = '#bot-test'


class AllUsersAvgJob(Job):
    """
    Every few seconds, calculates the avg of the numbers of all of the users and sends it to the chat
    """

    def __init__(self, interval, channel, users_numbers_json_path):
        super(AllUsersAvgJob, self).__init__(interval)
        self._channel = channel
        self._users_numbers_json_path = users_numbers_json_path

    def _check_if_there_were_new_numbers_since_last_time(self):
        """
        Checks if the json with the users' numbers has changed since the last time the job had ran
        :return: True if the jscn has changed and False if not
        """
        last_updated = os.path.getmtime(self._users_numbers_json_path)
        return time.time() < last_updated + self.interval

    def _get_all_users_avg(self):
        """
        Calculates the avg of the users' numbers from the json
        :return: the avg of the numbers
        """
        with open(self._users_numbers_json_path, 'rb') as f:
            users_numbers_dict = json.load(f)
        return calculate_avg_of_all_users_numbers(users_numbers_dict)

    def run(self, slack_client):
        """
        Checks if there were new messages since the last time the job had ran, calculates the numbers' avg and sends it
        to the public channel
        :param slack_client: the slack_client instance from the plugin
        :return: the output to the chat
        """
        if not self._check_if_there_were_new_numbers_since_last_time():
            return []
        users_avg = self._get_all_users_avg()
        return [[self._channel, "All users average: {avg}".format(avg=users_avg)]]


class AllUsersAvgPlugin(Plugin):
    """
    Initials a job which calculates the avg of the users' numbers
    """

    def register_jobs(self):
        job = AllUsersAvgJob(JOB_INTERVAL, CHANNEL, USERS_AVG_JSON_PATH)
        self.jobs.append(job)
