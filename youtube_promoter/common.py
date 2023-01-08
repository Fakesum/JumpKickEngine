from .utils.tomlsettings.tomlsettings import settings as settings
from .utils import poll_decorator, find_free_port
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

def wrap_filter(f):
    def wrapper(args, common=[]):
        for arg in args:
            yield f(arg, *common)
    def _wrapper(args, common=[]):
        return list(wrapper(args, common))
    return _wrapper
def start_server() -> int:
    """Start Flask Server

    Returns:
        int: port that the server is runing at
    """
    from .server import Server
    port = find_free_port()
    Server(settings["local"]["vid_ids"],port,settings["local"]["num_vid_insts"]).start()
