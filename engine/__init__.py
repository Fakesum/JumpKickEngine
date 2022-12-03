from . import server as __server
from .utils import find_free_port as __find_free_port
from .utils import exec_cmd as __exec_cmd

def __run(server: __server.Server, port, config, debug):
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By

    import os, time

    display = None
    if os.name == 'posix':
        from pyvirtualdisplay.display import Display
        # display = Display()
        # display.start()
    
    server.start()

    def run_time():
        options = uc.ChromeOptions()
        options.add_argument("--mute-audio")
        options.add_argument("--disable-dev-shm-usage")

        driver = uc.Chrome(
            options=options,
            no_sandbox=(False if debug else True),
            version_main=((int(__exec_cmd("google-chrome-stable --version")[0].split(" ")[-2].split(".")[0])) if debug else None),
            driver_executable_path=(None if debug else "/usr/bin/chromedriver")
        )

        print("Started Driver")

        while True:
            driver.get(f"http://localhost:{port}")

            for frame in driver.find_elements(By.CSS_SELECTOR, "iframe"):
                driver.switch_to.frame(frame)
                driver.find_element(By.CSS_SELECTOR, """button[aria-label="Play"]""").click()
                driver.switch_to.default_content()
            
            time.sleep(60)
    
    import threading
    threads = []

    for _ in range(config["dnum"]):
        threads.append(threading.Thread(target=run_time))
    
    for thread in threads: thread.start()
    for thread in threads:thread.join()

def start(config: str, debug = True) -> None:
    port = __find_free_port()

    import toml
    __run(__server.Server(toml.load(config), port), port, toml.load(config), debug)
