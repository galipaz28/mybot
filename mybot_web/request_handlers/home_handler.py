from webapp2 import RequestHandler


class HomeHandler(RequestHandler):

    def get(self):
        self.response.write('Hello!')

