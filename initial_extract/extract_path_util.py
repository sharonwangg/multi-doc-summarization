import os
from path_util import DATA_PATH


def get_summary_path(topic):
    """
    Args:
        topic (str): Topic of summary.

    Returns:
        (str): Path of extracted summary.
    """
    return os.path.join(DATA_PATH, 'step2_initial_extraction', topic + '_initial_summary.txt')


def get_extracted_dates_path(topic):
    """
    Args:
        topic (str): Topic of summary.

    Returns:
        (str): Path of extracted dates.
    """
    return os.path.join(DATA_PATH, topic + '_initial_summary_dates.txt')