from webapp2 import RequestHandler
from mybot.utils import calculate_user_numbers_avg
from mybot.config import USERS_AVG_JSON_PATH
import json


class UserAvgHandler(RequestHandler):

    @staticmethod
    def _get_users_dict():
        with open(USERS_AVG_JSON_PATH, 'rb') as f:
            return json.load(f)

    def get(self, user_name):
        users_numbers_dict = self._get_users_dict()
        if user_name not in users_numbers_dict:
            response_string = 'User {user_name} does not exist.'.format(user_name=user_name)
        else:
            user_avg = calculate_user_numbers_avg(users_numbers_dict, user_name)
            response_string = 'The average of user {user_name} is {avg}'.format(user_name=user_name, avg=user_avg)
        self.response.write(response_string)
