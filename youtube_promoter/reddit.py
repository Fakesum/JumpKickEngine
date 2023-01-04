from .base import YoutubeBot

class YoutubeViewBot(YoutubeBot):
    from .common import (
        wrap_poll,
        wrap_filter,
        By
    )
    def __init__(self) -> None:
        super().__init__()
        self.valid_subreddits = ["JumpKickEngine", "JumpKickEngine1"]

    @wrap_poll(None, validity_determiner=(lambda a: a != []))
    def __get_vids(self):
        return self.driver.find_elements(self.By.CSS_SELECTOR, "iframe.media-element")
    
    def run(self):
        self.create_driver()

        @self.wrap_filter
        @self.wrap_poll(None, expected_outcome=None)
        def play_vids(frame):
            self.driver.switch_to.frame(frame)
            self.play_vids("iframe")

        for subreddit in self.valid_subreddits:
            self.driver.get(f"https://reddit.com/r/{subreddit}")
            play_vids(self.__get_vids())

            if subreddit != self.valid_subreddits[-1]:
                self.driver.switch_to.new_window()

        import time 
        while True:
            time.sleep(40)
            for window in self.driver.window_handles:
                self.driver.switch_to.window(window)
                self.driver.get(self.driver.current_url)

                play_vids(self.__get_vids())
