import threading

class RoundTable(list):
    shift: int = 1
    prev: int = 0

    def get(self, num: int, iterations):
        for _ in range(iterations):
            if self.prev >= self.__len__():
                self.prev = self.prev - self.__len__()
            self.prev += self.shift
        
        if (self[self.prev:num+self.prev].__len__() < num):
            q, r = divmod(num+self.prev, self.__len__())
            nlist = q*self+self[:r]
            if nlist.__len__() >= num:
                return nlist[nlist.__len__() - num: -1]
            else:
                return nlist
        else:
            return self[self.prev:num+self.prev]

class Server(threading.Thread):
    def __init__(self, vid_ids: list, port, vids_insts) -> None:
        self.vids = RoundTable(vid_ids)
        self.nthcall = 0

        self.VIDS_INST = vids_insts

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
            """ + (" ".join([f"""<iframe width="90" height="160" src="https://www.youtube.com/embed/{vid}"></iframe>""" for vid in self.vids.get(self.VIDS_INST+1, self.nthcall)])) +"""
            </body>
            </html>
            """
            self.nthcall += 1
            return flask.render_template_string(TO_RENDER)

        app.run(port=self.port)