import logging
import atexit
from colorlog import ColoredFormatter

file_handler = None  # Global variable

def setup_logging():
    global file_handler

    formatter = ColoredFormatter(
        '%(asctime)s %(log_color)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'white',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
            'TWITCH': 'purple',
            'YOUTUBE': 'red',
        }
    )

    logging.addLevelName(25, 'TWITCH')
    logging.addLevelName(21, 'YOUTUBE')

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(filename="stream.log", encoding="utf-8", mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        handlers=[stream_handler, file_handler], level=logging.INFO
    )

    atexit.register(close_log_handlers)

def close_log_handlers():
    global file_handler
    if file_handler:
        logging.getLogger().removeHandler(file_handler)
        file_handler.close()
        file_handler = None