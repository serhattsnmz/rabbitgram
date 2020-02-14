import os
import logging
import logging.handlers
import yaml

import rabbitgram.statics as st

"""
LOGGING LEVELS :
    CRITICAL    = 50
    ERROR       = 40
    WARNING     = 30
    INFO        = 20
    DEBUG       = 10
    NOTSET      = 0
"""

class Logger:

    def __init__(self):
        self.settings = self.get_settings(st.SETTINGS_FILE_PATH)

    def get_settings(self, file_path):
        with open(file_path) as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def create_logger(self, app_name):

        # CREATE LOGGER INSTANCE AND SET LEVEL
        logger = logging.getLogger(app_name)
        logger.setLevel(logging.DEBUG)

        # STREAM HANDLER
        try:
            settings = self.settings["logger_settings"]["stream_handler"]
            if settings["status"]:
                console_handler = logging.StreamHandler()
                console_handler.setLevel(settings["level"])
                console_handler.setFormatter(logging.Formatter(settings["format"], datefmt='%Y-%m-%d %H:%M:%S'))
                logger.addHandler(console_handler)
        except KeyError:
            pass
        except Exception as exp:
            raise(exp)

        # HTTP HANDLER
        try:
            settings = self.settings["logger_settings"]["http_handler"]
            if settings["status"]:
                http = logging.handlers.HTTPHandler(settings["server"], settings["endpoint"], method=settings["method"])
                http.setLevel(settings["level"])
                logger.addHandler(http)
        except KeyError:
            pass
        except Exception as exp:
            raise(exp)

        # FILE HANDLER
        try:
            settings = self.settings["logger_settings"]["file_handler"]

            # Create file if does not exists
            if settings["status"] and not os.path.exists(os.path.dirname(settings["logfile_file_path"])):
                os.makedirs(os.path.dirname(settings["logfile_file_path"]))

            if settings["status"]:
                file_handler = logging.handlers.RotatingFileHandler(settings["logfile_file_path"], maxBytes = settings["file_max_size"], backupCount=settings["file_backup_count"])
                file_handler.setLevel(settings["level"])
                file_handler.setFormatter(logging.Formatter(settings["format"], datefmt='%Y-%m-%d %H:%M:%S'))
                logger.addHandler(file_handler)
        except KeyError:
            pass
        except Exception as exp:
            raise(exp)

        return logger