import threading, typing, time
from utils import wrap_poll, exec_cmd, wrap_filter, find_free_port, settings
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

class YoutubeBot(threading.Thread):
    import os as __os

    def __init__(self) -> None:

        self.__display = None

        super().__init__()
        self.daemon = True

    def create_driver(self) -> None:
        """
            Create Undetected Chromedriver for any given Env
        """
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
            no_sandbox=(False if settings["debug"] else True),
            version_main=((int(exec_cmd("google-chrome-stable --version")[0].split(" ")[-2].split(".")[0])) if settings["debug"] else None),
            driver_executable_path=(None if settings["debug"] else "/usr/bin/chromedriver")
        )

    def __default_content(self):
        self.driver.switch_to.default_content()

    @wrap_poll(None, poll=1, expected_outcome=None, on_failer=__default_content)
    def play_vids(self, vid_sel: str)->None:
        self.driver.switch_to.frame(self.driver.find_element(vid_sel))
        self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Play"]').click()
        self.driver.switch_to.default_content()

class YoutubeViewBot_Reddit(YoutubeBot):
    def __init__(self) -> None:
        super().__init__()
        self.valid_subreddits = ["JumpKickEngine", "JumpKickEngine1"]

    @wrap_poll(None, validity_determiner=(lambda a: a != []))
    def __get_vids(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "iframe.media-element")
    
    def run(self):
        self.create_driver()

        @wrap_filter
        @wrap_poll(None, expected_outcome=None)
        def play_vids(frame):
            self.driver.switch_to.frame(frame)
            self.play_vids("iframe")

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

    def __init__(self, vids: typing.List[str], port) -> None:
        super().__init__()
        self.VIDS = vids
        self.port = port
    
    @wrap_poll(None, validity_determiner=(lambda a: (a.__len__() == settings["local"]["num_vid_insts"])))
    def __get_vids(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "iframe")
    
    def run(self):
        """
            Main function of the parrelle selenium inst
        """
        import time
        
        self.create_driver()

        self.driver.get(f"http://localhost:{self.port}/")

        @wrap_filter
        def play_vids(frame):
            self.play_vids(frame)
        
        while True:
            play_vids(self.__get_vids())
            time.sleep(settings["wait_time"])
            self.driver.get(f"http://localhost:{self.port}/")

def main():
    """
        Starting point of the program
    """
    def start_server() -> int:
        """Start Flask Server

        Returns:
            int: port that the server is runing at
        """
        from server import Server
        port = find_free_port()
        Server(settings["local"]["vid_ids"],port,settings["local"]["num_vid_insts"]).start()

    match settings["type"]:
        case 0:
            [YoutubeViewBot_Reddit().start() for _ in range(settings["dnum"])]
        case 1:
            [YoutubeViewBot_Local(settings["local"]["vid_ids"], start_server()).start() for _ in range(settings["dnum"])]
    
    import time
    while True:
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        import sys
        sys.exit(1)