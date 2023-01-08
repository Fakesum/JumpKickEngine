from .base import YoutubeBot

class YoutubeViewBot(YoutubeBot):
    import typing

    from .common import (
        poll_decorator,
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
        self.create_driver()

        @self.poll_decorator(None, validity_determiner=(lambda a: (a.__len__() == self.settings["local"]["num_vid_insts"])))
        def __get_vids(self):
            return self.driver.find_elements(self.By.CSS_SELECTOR, "iframe")
        
        @self.wrap_filter
        def play_vids(frame):
            self.play_vids(frame)
        
        for _ in range(self.settings["tabs"]):
            self.driver.get(f"http://localhost:{self.port}/")
            play_vids(__get_vids())
            self.driver.switch_to.new_window()
        
        import time
        while True:
            time.sleep(self.settings["wait_time"])
            for i in range(self.settings["tabs"]):
                self.driver.switch_to.window(self.driver.window_handles[i])
                self.driver.get(f"http://localhost:{self.port}/")
                play_vids(__get_vids())