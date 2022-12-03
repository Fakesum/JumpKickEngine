import threading

class Server(threading.Thread):    
    def __init__(self, config, port) -> None:
        self.vids = config["video_ids"]
        self.port = port

        super().__init__()
        self.daemon = True

    def run(self):
        import flask

        app = flask.Flask(__name__)

        @app.route("/")
        def main():
            TO_RENDER = """
            <html>
            <body>
            """ + (" ".join([f"""<iframe width="90" height="160" src="https://www.youtube.com/embed/{vid}"></iframe>""" for vid in self.vids])) +"""
            </body>
            </html>
            """
            return flask.render_template_string(TO_RENDER)

        app.run(port=self.port)