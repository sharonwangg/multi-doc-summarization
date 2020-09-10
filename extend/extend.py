from data_util import NLP
from sentence_details import SentenceDetails

from organize_timeloc.organize import organized_summary
from initial_extract.extract import topic_to_phrase
from compress.compress import TOPIC
from organize_timeloc.location_util import valid_index

def extend(organized_summary, phrases):
    """
    Args:
        organized_summary (dict from str to list): Keys are countries. Values are a list of SentenceDetails.
        phrases (dict from str to list of str): Maps topics to their respective phrases.

    Returns:
    """
    #print(organized_summary.keys())
    for country, sentence_details in organized_summary.items():
        for sentence_detail in sentence_details:
            sentence = list(NLP(sentence_detail.text).sents)[0]
            print(sentence)
            print(sentence_detail.og_article[9])
            print(str(sentence)[0])
            print(str(sentence_detail.og_article[9])[0])
            print(sentence == sentence_detail.og_article[9])
            #for i, s in enumerate(sentence_detail.og_article):
                #print(str(i) + '\n')
                #print(str(s) + '\n' + '\n')
            if sentence in sentence_detail.og_article:
                center_idx = sentence_detail.og_article.index(sentence)
                print('center_idx: ' + str(center_idx))
                max_radius = max(center_idx, len(sentence_detail.og_article) - 1)
                for i in range(1, max_radius):
                    previous_idx = center_idx - i
                    if valid_index(previous_idx, sentence_detail.og_article):
                        print('previous_idx: ' + str(previous_idx))
                    future_idx = center_idx + i
                    if valid_index(future_idx, sentence_detail.og_article):
                        print('future_idx: ' + str(future_idx))

        return ""

                


final_summary = extend(organized_summary, topic_to_phrase[TOPIC])