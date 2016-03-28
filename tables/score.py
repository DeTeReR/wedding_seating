from functools import total_ordering


def _less_than(first, second):
    if first == second:
        return False
    if first is None:
        return True
    if second is None:
        return False
    return first < second


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
        return (_less_than(self.lowest_table_score, other.lowest_table_score)
                or _less_than(self.total, other.total)
                or _less_than(self.lowest_person_score, other.lowest_person_score))
