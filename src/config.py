"""
Global configurations.

Author: Shaowen Chen
Email: alvinchan2004@hotmail.com
Date: 2026-04-06
"""

import os
import pathlib

ROOT_PATH = pathlib.Path(__file__).parent.parent
LOG_PATH = os.path.join(ROOT_PATH, "logs")
LOG_FILE_PATH =  os.path.join(LOG_PATH,"Lunar.log")


DEBUG = True
