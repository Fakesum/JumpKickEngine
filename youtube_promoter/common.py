import utils.tomlsettings.settings as settings
from utils import exec_cmd, wrap_poll, wrap_filter, find_free_port
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

def start_server() -> int:
    """Start Flask Server

    Returns:
        int: port that the server is runing at
    """
    from server import Server
    port = find_free_port()
    Server(settings["local"]["vid_ids"],port,settings["local"]["num_vid_insts"]).start()
