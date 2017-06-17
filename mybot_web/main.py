from paste import httpserver
from webapp2 import Route, WSGIApplication
from request_handlers import UserAvgHandler, AllUsersAvgHandler, HomeHandler


app = WSGIApplication([
    Route(r'/', HomeHandler),
    Route(r'/average', AllUsersAvgHandler),
    Route(r'/average/<user_name>', UserAvgHandler)])


def main():
    httpserver.serve(app, host='127.0.0.1', port='8081')


if __name__ == '__main__':
    main()
