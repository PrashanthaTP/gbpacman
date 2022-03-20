from plogger import get_logger


global_logger = None
def get_global_logger():
    global global_logger
    if global_logger is None:
        global_logger = get_logger("gbpacman")
    return global_logger
