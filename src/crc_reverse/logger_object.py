# -*- coding: utf-8 -*-
"""
Created on Fri May  6 21:18:05 2022

@author: DanielT17
"""

# %% Imports

from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING, Formatter, Logger, LogRecord, StreamHandler, getLogger

# %% Functions

class custom_formatter(Formatter):
    """
    Description:
        This function configurates the logger object.
    Inputs:
        logging.Formatter - logging - logging foramatter.
    Outputs:
        formatter.format(record) - formatter - recorded dictionary turns it to string.
    """
    grey = "\x1b[38;20m"; green = "\x1b[32;1m"; yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"; bold_red = "\x1b[31;1m"; reset = "\x1b[0m"
    base_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    FORMATS = {
        DEBUG: grey + base_format + reset,
        INFO: green + base_format + reset,
        WARNING: yellow + base_format + reset,
        ERROR: red + base_format + reset,
        CRITICAL: bold_red + base_format + reset,
    }

    def format(self, record: LogRecord) -> str:
        """Apply level-specific color formatting to a single log record."""
        log_fmt = self.FORMATS.get(record.levelno, self.base_format)
        formatter = Formatter(log_fmt)
        return formatter.format(record)

def logger_object() -> Logger:
    """
    Description:
        This function creates and configurates the logger object.
    Inputs:
        None.
    Outputs:
        logger - logging module - a logging object configured.
    """
    logger = getLogger("CRC reversing")
    logger.setLevel(DEBUG)
    ch = StreamHandler()
    ch.setLevel(DEBUG)
    ch.setFormatter(custom_formatter())
    if not logger.handlers:
        logger.addHandler(ch)
    return logger
