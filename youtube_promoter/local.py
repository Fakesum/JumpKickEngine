from .base import YoutubeBot

class YoutubeViewBot(YoutubeBot):
    import typing

    def __init__(self, vids: typing.List[str], port) -> None:
        super().__init__()
        self.VIDS = vids
        self.port = port
    
    def run(self):
        """
            Main function of the parrelle selenium inst
        """
        from .common import (
            poll_decorator,
            wrap_filter
        )
        self.create_driver()

        @poll_decorator(None)
        def __get_vids():
            return self.driver.find_elements(self.By.CSS_SELECTOR, "iframe")
        
        @wrap_filter
        def play_videos(frame):
            self.play_vids(frame)
        
        for _ in range(self.settings["local"]["tabs"]):
            self.driver.get(f"http://localhost:{self.port}/")
            play_videos(__get_vids())
            self.driver.switch_to.new_window()
        
        import time
        while True:
            time.sleep(self.settings["wait_time"])
            for i in range(self.settings["tabs"]):
                self.driver.switch_to.window(self.driver.window_handles[i])
                self.driver.get(f"http://localhost:{self.port}/")
                play_videos(__get_vids())