# -*- coding: utf-8 -*-
"""
Created on Fri May  6 21:18:05 2022

@author: DanielT17
"""

# %% Imports

from logging import Formatter,DEBUG,INFO,WARNING,ERROR,CRITICAL,getLogger,StreamHandler

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
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    FORMATS = {DEBUG: grey + format + reset, 
               INFO: green + format + reset, 
               WARNING: yellow + format + reset, 
               ERROR: red + format + reset, 
               CRITICAL: bold_red + format + reset}

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = Formatter(log_fmt)
        return formatter.format(record)

def logger_object():
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
    logger.addHandler(ch)
    return logger