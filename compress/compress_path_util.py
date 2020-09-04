import os
from path_util import DATA_PATH

def get_compressed_summary_path(topic):
    return os.path.join(DATA_PATH, 'step3_compressed_summary', topic + '_compressed_summary.txt')