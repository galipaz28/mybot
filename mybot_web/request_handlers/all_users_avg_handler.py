from webapp2 import RequestHandler
from mybot.utils import calculate_avg_of_all_users_numbers
from mybot.config import USERS_AVG_JSON_PATH
import json


class AllUsersAvgHandler(RequestHandler):

    @staticmethod
    def _get_all_users_avg():
        with open(USERS_AVG_JSON_PATH, 'rb') as f:
            users_numbers = json.load(f)
        return calculate_avg_of_all_users_numbers(users_numbers)

    def get(self):
        users_numbers_avg = self._get_all_users_avg()
        self.response.write('This is the average of all users numbers: {avg}'.format(avg=users_numbers_avg))
