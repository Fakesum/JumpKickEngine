import threading as __threading
class Bot(__threading.Thread):
    def __init__(self, colab: bool=True, logging=True) -> None:
        self.__display = None

        self.colab: bool = colab
        self.logging = logging

        from .archive import active_subreddits
        self.active_subreddits = active_subreddits

        super().__init__()
        self.daemon = True

    def run(self) -> None:
        import undetected_chromedriver as uc
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.action_chains import ActionChains
        from .utils import wrap_poll, exec_cmd, wrap_filter

        from loguru import logger
        if not self.logging:
            logger.remove()
        logger.info("Started")

        def init_driver():
            import os
            if os.name == "posix":
                from pyvirtualdisplay.display import Display
                self.__display = Display()
                self.__display.start()
            
            options = uc.ChromeOptions()
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--mute-audio")
            options.add_argument("--disable-notifications")

            if self.colab:
                return uc.Chrome(
                    options=options,
                    version_main= int(exec_cmd("google-chrome-stable --version")[0].split(" ")[-2].split(".")[0]), # ex, 106 or 107
                    no_sandbox=False
                )
            else:
                return uc.Chrome(options=options, no_sandbox=False, driver_executable_path="/usr/bin/chromedriver")
        
        @wrap_filter
        @wrap_poll(None, poll=None, return_val=True, fast=True, on_failer=(lambda: driver.switch_to.default_content()), error_logger=print)
        def play_videos(video, driver: uc.Chrome):
            driver.execute_script("""arguments[0].scrollIntoView();""", video)
            
            driver.switch_to.frame(video)
            driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, 'iframe'))
            
            ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, '#movie_player > div.ytp-cued-thumbnail-overlay > button')).click().perform()
            logger.debug("Played Video")
            driver.switch_to.default_content()

        
        driver = init_driver()
        logger.info("Driver Created")


        for rep in self.active_subreddits:
            driver.get(f"https://reddit.com/r/{rep}")

            driver.switch_to.default_content()
            
            play_videos(driver.find_elements(By.CSS_SELECTOR, 'iframe.media-element'), common=driver)
             
            if rep != self.active_subreddits[-1]: driver.switch_to.new_window()
            
        
        logger.info("Starting MainLoop")
        import time
        while True:
            time.sleep(40)
            for tab in driver.window_handles:
                driver.switch_to.window(tab)

                for frame in driver.find_elements(By.CSS_SELECTOR, 'iframe.media-element'):
                    driver.execute_script("arguments[0].src = arguments[0].src", frame)
                
                logger.debug("reloaded youtube iframe")

                driver.switch_to.default_content()
                play_videos(driver.find_elements(By.CSS_SELECTOR, 'iframe.media-element'), common=driver)

                logger.debug("waiting for 40 seconds")
        
        logger.warning("Ending of a While True loop has been reached")
        logger.warning("Under Normal Surcomestances this should be impossible")
        return None
