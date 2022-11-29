import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from engine.utils import exec_cmd


def main():
    options = uc.ChromeOptions()
    options.add_argument("--mute-audio")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.page_load_strategy = "none"

    driver = uc.Chrome(options=options, version_main=int(exec_cmd("google-chrome-stable --version")[0].split(" ")[-2].split(".")[0]))

    for subreddit in ["JumpkickEngine", "JumpkickEngine1"]:
        driver.get(f"https://reddit.com/r/{subreddit}")
        for video in driver.find_elements(By.CSS_SELECTOR, 'iframe.media-element'):
            driver.switch_to.frame(video)
            driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, 'iframe'))
            ActionChains(driver).click(driver.find_element(By.CSS_SELECTOR, '#movie_player > div.ytp-cued-thumbnail-overlay > button')).perform()
    time.sleep(50)

if __name__ == "__main__":
    from engine.utils import wrap_poll, timeit

    @timeit
    @wrap_poll(1, poll=None, return_val=True, fast=True, error_logging=True)
    def main():
        import random
        return 1 / random.choice([1, 0])
    
    print(main())