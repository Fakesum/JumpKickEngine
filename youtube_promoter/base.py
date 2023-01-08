import threading as __threading

class YoutubeBot(__threading.Thread):
    from .common import (
        settings,
        poll_decorator,
        uc,
        By
    )
    import os as __os

    def __init__(self) -> None:

        self.__display = None

        super().__init__()
        self.daemon = True

    def create_driver(self) -> None:
        """
            Create Undetected Chromedriver for any given Env
        """
        options = self.uc.ChromeOptions()

        if self.settings["headless"]:
            options.add_argument("--headless")
        elif (self.__os.name == 'posix') and self.settings["VD"]:
            from pyvirtualdisplay.display import Display
            self.__display = Display()
            self.__display.start()
        
        options.add_argument("--mute-audio")
        options.add_argument("--disable-dev-shm-usage")

        from .utils import exec_cmd

        self.driver: self.uc.Chrome = self.uc.Chrome(
            options=options,
            no_sandbox=(False if self.settings["debug"] else True),
            version_main=((int(exec_cmd("google-chrome-stable --version")[0].split(" ")[-2].split(".")[0])) if self.settings["debug"] else None),
            driver_executable_path=(None if self.settings["debug"] else "/usr/bin/chromedriver")
        )

    @poll_decorator(None, return_val="validation", validation="expected_outcome",expected_outcome=None)
    def play_vids(self, vid_sel: str)->None:
        try:
            self.driver.switch_to.frame(vid_sel)
            self.driver.find_element(self.By.CSS_SELECTOR, '[aria-label="Play"]').click()
        finally:
            self.driver.switch_to.default_content()