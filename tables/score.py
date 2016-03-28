from functools import total_ordering


@total_ordering
class Score(object):
    def __init__(self, total=None, lowest_table_score=None, lowest_person_score=None):
        self.total = total
        self.lowest_table_score = lowest_table_score
        self.lowest_person_score = lowest_person_score

    def __eq__(self, other):
        return self.total == other.total and \
               self.lowest_person_score == other.lowest_person_score and \
               self.lowest_table_score == other.lowest_table_score

    def __lt__(self, other):
        return self.lowest_table_score < other.lowest_table_score \
               or (self.lowest_table_score == other.lowest_table_score and self.total < other.total) \
               or (self.lowest_table_score == other.lowest_table_score
                   and self.total == other.total
                   and self.lowest_person_score < other.lowest_person_score)
