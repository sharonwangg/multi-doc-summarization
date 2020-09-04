from organize.organize import organized_summary
from initial_extract.extract import topic_to_phrase
from compress.compress import TOPIC
from data_util import NLP


def extend(organized_summary, phrases):
    for country, sentence_details in organized_summary:
        for sentence_detail in sentence_details:
            doc = NLP(sentence_detail.text)
            sentence = list(doc.sents)
            if len(sentence) != 1:
                continue

            str_og_article = ''
            for sent in sentence_detail.og_article:
                str_og_article += (' ' + str(sent) + ' ')

            sentence = sentence[0]
            print(sentence)
            if sentence in sentence_detail.og_article:
                center_idx = sentence_detail.og_article.index(sentence)
                


final_summary = extend(organized_summary, topic_to_phrase[TOPIC])