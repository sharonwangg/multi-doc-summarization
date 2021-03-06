"""
Utility module for storing paths for organize.py.

Attributes:
    ORGANIZED_SUMMARY_PATH (str): Path for location and time-organized summary.
"""
import os
from path_util import DATA_PATH
from compress.compress_data_util import TOPIC

ORGANIZED_SUMMARY_PATH = os.path.join(DATA_PATH, 'step4_organized_summary', TOPIC + '_organized_summary.txt')
