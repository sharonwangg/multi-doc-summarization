class SentenceDetails:
    def __init__(self, text, date, relevancy_score, og_article):
        """
        Args:
            text (str): Sentence text.
            date (str): Date. YYYY-MM-DD.
            relevancy_score (float): Cosine similarity between `text` and topic.
            og_article (str): Original article that `text` is from.
        """
        self._text = text
        self._date = date
        self._relevancy_score = relevancy_score
        self._og_article = og_article

    @property
    def text(self):
        return self._text

    @property
    def date(self):
        return self._date

    @property
    def relevancy_score(self):
        return self._relevancy_score

    @property
    def og_article(self):
        return self._og_article
