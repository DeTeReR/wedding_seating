from functools import total_ordering


def _less_than(first, second):
    if first == second:
        return False
    if first is None:
        return True
    if second is None:
        return False
    return first < second


def _score_difference_multiplier(old, new):
    new = 0 if new is None else new
    old = 1 if old is None or old == 0 else old
    return 1 - ((old - new) / old)


@total_ordering
class Score(object):
    _SCORE_PRECEDENTS = ('lowest_table_score', 'total', 'lowest_person_score')

    def __init__(self, total=None, lowest_table_score=None, lowest_person_score=None):
        self.total = total
        self.lowest_table_score = lowest_table_score
        self.lowest_person_score = lowest_person_score

    def __repr__(self):
        return '%s(lowest_table_score=%s, total=%s, lowest_person_score=%s)' % \
               tuple([self.__class__.__name__] + list(getattr(self, sub_score) for sub_score in self._SCORE_PRECEDENTS))

    def __eq__(self, other):
        return all(getattr(self, sub_score) == getattr(other, sub_score) for sub_score in self._SCORE_PRECEDENTS)

    def _scores_in_order(self, other):
        for sub_score in self._SCORE_PRECEDENTS:
            self_score = getattr(self, sub_score)
            other_score = getattr(other, sub_score)
            yield self_score, other_score

    def __lt__(self, other):
        for self_score, other_score in self._scores_in_order(other):
            if _less_than(self_score, other_score):
                return True
            elif self_score != other_score:
                return False
        return False

    def difference_multiplier(self, other):
        """
        Method to give a measure of how close two scores are.
        1: self == other
        0: other == 0
        >1: other > self
        """
        for self_score, other_score in self._scores_in_order(other):
            if self_score != other_score:
                return _score_difference_multiplier(self_score, other_score)
        return 1