import threading, typing, time
from utils import wrap_poll, exec_cmd, wrap_filter, find_free_port, settings
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

class YoutubeBot(threading.Thread):
    import os as __os

    DEBUG = True

    def __init__(self) -> None:

        self.__display = None

        super().__init__()
        self.daemon = True

    def create_driver(self) -> None:
        options = uc.ChromeOptions()

        if settings["headless"]:
            options.add_argument("--headless")
        elif (self.__os.name == 'posix'):
            from pyvirtualdisplay.display import Display
            self.__display = Display()
            self.__display.start()
        
        options.add_argument("--mute-audio")
        options.add_argument("--disable-dev-shm-usage")

        self.driver: uc.Chrome = uc.Chrome(
            options=options,
            no_sandbox=(False if self.DEBUG else True),
            version_main=((int(exec_cmd("google-chrome-stable --version")[0].split(" ")[-2].split(".")[0])) if self.DEBUG else None),
            driver_executable_path=(None if self.DEBUG else "/usr/bin/chromedriver")
        )

class YoutubeViewBot_Reddit(YoutubeBot):
    def __init__(self) -> None:
        super().__init__()
        self.valid_subreddits = ["JumpKickEngine", "JumpKickEngine1"]

    @wrap_poll(None, validity_determiner=(lambda a: a != []))
    def __get_vids(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "iframe.media-element")
    
    def __default_content(self):
        self.driver.switch_to.default_content()
    
    @wrap_poll(None, expected_outcome=None, on_failer=__default_content)
    def __switch_video_frame(self, frame):
        self.driver.switch_to.frame(frame)
        self.driver.switch_to.frame(self.driver.find_element(By.CSS_SELECTOR, "iframe"))
    
    @wrap_poll(None, expected_outcome=None)
    def __press_play_vids(self):
        self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Play"]').click()

    
    def run(self):
        self.create_driver()

        @wrap_filter
        def play_vids(frame):
            self.__switch_video_frame(frame)
            self.__press_play_vids()
            self.__default_content()

        for subreddit in self.valid_subreddits:
            self.driver.get(f"https://reddit.com/r/{subreddit}")
            play_vids(self.__get_vids())

            if subreddit != self.valid_subreddits[-1]:
                self.driver.switch_to.new_window()
        
        while True:
            time.sleep(40)
            for window in self.driver.window_handles:
                self.driver.switch_to.window(window)
                self.driver.get(self.driver.current_url)

                play_vids(self.__get_vids())

class YoutubeViewBot_Local(YoutubeBot):
    from selenium.webdriver.common.action_chains import ActionChains

    def __init__(self, vids: typing.List[str]) -> None:
        super().__init__()
        self.VIDS = vids
    
    @wrap_poll(None, validity_determiner=(lambda a: (a.__len__() == settings["local"]["num_vid_insts"])))
    def __get_vids(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "iframe")
    
    @wrap_poll(None, expected_outcome=None)
    def __switch_to_frame(self, frame):
        self.driver.switch_to.frame(frame)
    
    def __play_vid(self):
        self.ActionChains(self.driver).click(self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Play"]')).perform()
    
    def run(self):
        from server import Server
        import time

        port = find_free_port()
        server = Server(self.VIDS, port, settings["local"]["num_vid_insts"])
        server.start()
        
        self.create_driver()

        self.driver.get(f"http://localhost:{port}/")

        @wrap_filter
        def play_vids(frame):
            self.__switch_to_frame(frame)
            self.__play_vid()
            self.driver.switch_to.default_content()
        
        while True:
            play_vids(self.__get_vids())
            time.sleep(settings["wait_time"])
            self.driver.get(f"http://localhost:{port}/")

def main():
    match settings["type"]:
        case 0:
            [YoutubeViewBot_Reddit().start() for _ in range(settings["dnum"])]
        case 1:
            [YoutubeViewBot_Local(settings["local"]["vid_ids"]).start() for _ in range(settings["dnum"])]
    
    import time
    while True:
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        import sys
        sys.exit(1)