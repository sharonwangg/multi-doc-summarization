"""
Utility module for loading data for compress.py.
"""
from initial_extract.extract import relevancy_sorted_all_sentence_details

WMD_THRESHOLD = 1.51
TOPICS = relevancy_sorted_all_sentence_details.keys()
TOPIC = 'symptom'

