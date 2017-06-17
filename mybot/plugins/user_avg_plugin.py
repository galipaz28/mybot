import json
from collections import defaultdict

from rtmbot.core import Plugin

from config import USERS_AVG_JSON_PATH
from utils import calculate_user_numbers_avg


CLEAN_DATA_HISTORY = True


class UserAvgPlugin(Plugin):
    """
    Calculates the avg of the numbers from the messages of each user
    """

    def __init__(self, name=None, slack_client=None, plugin_config=None, clean_data_history=CLEAN_DATA_HISTORY,
                 users_numbers_json_path=USERS_AVG_JSON_PATH):
        super(UserAvgPlugin, self).__init__(name, slack_client, plugin_config)
        self._clean_data_history = clean_data_history
        self._users_numbers_json_path = users_numbers_json_path
        self._users_numbers = self._create_users_numbers_dict()
        self._user_id_to_user_name = {}

    def _create_users_numbers_dict(self):
        if self._clean_data_history:
            users_dict = {}
        else:
            # if not clean data history, loads the json and uses its data
            with open(self._users_numbers_json_path, 'rb') as f:
                users_dict = json.load(f)
        return defaultdict(self._initial_user_data_factory, users_dict)

    @staticmethod
    def _initial_user_data_factory():
        return {'sum': 0.0, 'counter': 0.0}

    def _save_users_data_to_json(self):
        """
        Saves the dict with the new numbers of the users to the json file
        """
        with open(self._users_numbers_json_path, 'wb') as f:
            json.dump(dict(self._users_numbers), f)

    def _add_data_to_user(self, user, number):
        """
        Adds the new number of the user to the user's avg data
        :param user: the user_id of the user who wrote the number
        :param number: the number in the user's message
        """
        self._users_numbers[user]['sum'] += number
        self._users_numbers[user]['counter'] += 1
        self._save_users_data_to_json()

    def _get_user_avg(self, user):
        """
        Calculates the avg of the user's numbers
        :param user: the user_id to get his avg
        :return: the avg of the user's numbers
        """
        return calculate_user_numbers_avg(self._users_numbers, user)

    @staticmethod
    def _check_message_is_number(message):
        """
        Checks if the data of a message is a number or not
        :param message: the data of the message
        :return: True if the message is a number and False if not
        """
        try:
            float(message)
            return True
        except ValueError:
            return False

    def _get_user_name_from_user_id_by_slack_client(self, user_id):
        """
        Gets the user name from the user id by api call from the slack client
        :param user_id: the user id to get his user name
        :return: the user name
        """
        user_info = self.slack_client.api_call('users.info', user=user_id)
        if not user_info['ok']:
            return
        user_name = user_info['user']['name']
        self._user_id_to_user_name[user_id] = user_name
        return user_name

    def _get_user_name_from_user_id(self, user_id):
        """
        Gets the user name of a user id
        :param user_id: the user id to get his user name
        :return: the user name
        """
        if user_id in self._user_id_to_user_name.keys():
            return self._user_id_to_user_name[user_id]
        return self._get_user_name_from_user_id_by_slack_client(user_id)

    def process_message(self, data):
        """
        For each message in the chat, calculates the user's numbers avg and sends it to the chat
        :param data: the message in the chat
        """
        if not self._check_message_is_number(data['text']):
            return
        user_name = self._get_user_name_from_user_id(data['user'])
        self._add_data_to_user(user_name, float(data['text']))
        self.outputs.append([data['channel'], str(self._get_user_avg(user_name))])
