from unittest import TestCase

from tables.score import Score


class TestScore(TestCase):
    def test_comparisons(self):
        self.assertTrue(Score() == Score())
        self.assertTrue(Score(total=1) > Score())
        self.assertTrue(Score() < Score(total=1))

        self.assertTrue(Score(lowest_table_score=1, total=1) > Score(total=1))

        self.assertTrue(Score(lowest_table_score=100, total=1) > Score(lowest_table_score=100, total=0))
        self.assertTrue(
            Score(lowest_table_score=100, total=1, lowest_person_score=2) >
            Score(lowest_table_score=100, total=1, lowest_person_score=1))
        self.assertFalse(
            Score(lowest_table_score=2, total=1) < Score(lowest_table_score=1, total=2))