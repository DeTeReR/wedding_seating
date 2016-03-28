class Score(object):
    def __init__(self, total=None, lowest_table_score=None, lowest_person_score=None):
        self._total = total
        self._lowest_table_score = lowest_table_score
        self._lowest_person_score = lowest_person_score

    def __cmp__(self, other):
