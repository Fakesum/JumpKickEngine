from .base import YoutubeBot

class YoutubeViewBot(YoutubeBot):
    import typing

    from .common import (
        wrap_poll,
        settings,
        wrap_filter
    )

    def __init__(self, vids: typing.List[str], port) -> None:
        super().__init__()
        self.VIDS = vids
        self.port = port
    
    def run(self):
        """
            Main function of the parrelle selenium inst
        """
        import time
        
        self.create_driver()

        self.driver.get(f"http://localhost:{self.port}/")

        @self.wrap_poll(None, validity_determiner=(lambda a: (a.__len__() == self.settings["local"]["num_vid_insts"])))
        def __get_vids(self):
            return self.driver.find_elements(self.By.CSS_SELECTOR, "iframe")
        
        @self.wrap_filter
        def play_vids(frame):
            self.play_vids(frame)
        
        while True:
            play_vids(__get_vids())
            time.sleep(self.settings["wait_time"])
            self.driver.get(f"http://localhost:{self.port}/")
