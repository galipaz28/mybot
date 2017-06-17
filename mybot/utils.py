
def calculate_user_numbers_avg(users_numbers_info, user_name):
    """
    Calculates the average of the user's numbers
    :param users_numbers_info: dict with info on the users' numbers (dict with sum and counter)
    :param user_name: the user name of the user to calculate his avg
    :return: the avg of the user's numbers
    """
    return users_numbers_info[user_name]['sum'] / float(users_numbers_info[user_name]['counter'])


def calculate_avg_of_all_users_numbers(users_numbers_info):
    """
    Calculates the average of all the users' numbers
    :param users_numbers_info: dict with info on the users' numbers (dict with sum and counter)
    :return: the avg of all the users' numbers
    """
    users_numbers_sum = sum(user['sum'] for user in users_numbers_info.values())
    users_numbers_counter = sum(user['counter'] for user in users_numbers_info.values())
    return users_numbers_sum / float(users_numbers_counter)
