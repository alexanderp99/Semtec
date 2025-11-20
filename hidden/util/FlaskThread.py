import threading
from werkzeug.serving import make_server

class FlaskThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server("localhost", 8001, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()

