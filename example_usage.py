# -*- coding: utf-8 -*-
"""
Created on Sat May 14 18:56:04 2022

@author: danie
"""


# %% Imports

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from crc_reverse import crc_reversing

# %% Main

if __name__ == '__main__':
    crc_reversing()
