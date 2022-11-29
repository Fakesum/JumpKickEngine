import threading as __threading
class Bot(__threading.Thread):
    def __init__(self) -> None:
        self.__display = None

        from .archive import active_subreddits
        self.active_subreddits = active_subreddits

        super().__init__()
        self.daemon = True

    def run(self):
        import undetected_chromedriver as uc
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.action_chains import ActionChains
        from .utils import wrap_poll, exec_cmd, wrap_filter

        from loguru import logger
        logger.info("Started")

        @wrap_poll(None, poll=None, return_val=True, fast=True, error_logger=logger.warning)
        def init_driver():
            import os
            if os.name == "posix":
                from pyvirtualdisplay.display import Display
                self.__display = Display()
                self.__display.start()
            
            options = uc.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--mute-audio")
            options.add_argument("--disable-notifications")

            return uc.Chrome(options=options, version_main=int(exec_cmd("google-chrome-stable --version")[0].split(" ")[-2].split(".")[0]), no_sandbox=False)
        
        @wrap_filter
        @wrap_poll(None, poll=None, return_val=True, fast=True, on_failer=(lambda: driver.switch_to.default_content()), error_logger=logger.warning)
        def play_videos(video, driver: uc.Chrome):
            driver.execute_script("""arguments[0].scrollIntoView();""", video)
            
            logger.debug(("-"*5)+"Point"+("-"*5))

            driver.switch_to.frame(video)
            driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, 'iframe'))

            logger.debug(("-"*5)+"Point"+("-"*5))
            
            ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, '#movie_player > div.ytp-cued-thumbnail-overlay > button')).click().perform()
            driver.switch_to.default_content()

            logger.debug(("-"*5)+"Point"+("-"*5))
        
        driver = init_driver()
        logger.info("Driver Created")


        for rep in self.active_subreddits:
            logger.debug(("-"*5)+"Point"+("-"*5))
            driver.get(f"https://reddit.com/r/{rep}")

            driver.switch_to.default_content()
            logger.debug(("-"*5)+"Point"+("-"*5))
            
            play_videos(driver.find_elements(By.CSS_SELECTOR, 'iframe.media-element'), common=driver)
            
            logger.debug(("-"*5)+"Point"+("-"*5))
            
            if rep != self.active_subreddits[-1]: driver.switch_to.new_window()
            
            logger.debug(("-"*5)+"Point"+("-"*5))
        
        logger.info("Starting MainLoop")
        import time
        while True:
            time.sleep(40)
            for tab in driver.window_handles:
                driver.switch_to.window(tab)

                driver.execute_script("document.querySelectorAll('iframe.media-element')[0].src = document.querySelectorAll('iframe.media-element')[0].src")
                logger.debug("reloading youtube iframe")

                driver.switch_to.default_content()
                play_videos(driver.find_elements(By.CSS_SELECTOR, 'iframe.media-element'), common=driver)

                logger.debug("waiting for 40 seconds")
