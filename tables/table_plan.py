import itertools
import logging
import random
from functools import partial

from tables.table import Table, TableException

LOGGER = logging.getLogger(__name__)

def get_tens(people, relationships, the_one):
    return frozenset([person for person in people if relationships[frozenset([the_one, person])] == 10] + [the_one])


class TablePlan(object):
    def __init__(self, table_size=10, guest_count=130):
        num_tables = (guest_count//table_size) + 1
        max_sizes = [table_size] * num_tables
        capacity = table_size * num_tables
        seats_to_remove = capacity - guest_count
        if seats_to_remove % 2 == 1:
            max_sizes[-1] -= 1
            seats_to_remove -= 1
        for i in range(seats_to_remove//2):
            max_sizes[i] -= 2

        self._tables = set(Table(max_size=max_size) for max_size in max_sizes)

    def __str__(self):
        return 'TablePlan(_tables=%s)' % self._tables

    def seat_guests(self, guests):
        guest_index = 0
        for table in self._tables:
            for guest in guests[guest_index:guest_index + table.seat_count()]:
                table.add_guest(guest)
            guest_index += table.seat_count()

    def score(self, relationships):
        score = 0
        for table in self._tables:
            for pair_of_people in itertools.combinations(table.guests(), 2):
                score += relationships[frozenset(pair_of_people)]
        return score

    def state(self):
        return [table.state() for table in self._tables]

    def swap(self, relationships, count=1):
        for i in range(count):
            first_table, second_table = random.sample(self._tables, 2)
            first_table_people = self._pick_at_least_one_from_table(relationships, first_table, 1)
            second_table_people = set()
            safety = 0
            while len(first_table_people) != len(second_table_people):
                second_table_people = self._pick_at_least_one_from_table(relationships, second_table, len(first_table_people))
                safety += 1
                if safety > 3:
                    LOGGER.warning(
                        'Dodgey swap, split up couples:\n%s\n%s',
                        first_table.guests(),
                        second_table.guests())
                    second_table_people = list(second_table_people)[:len(first_table_people)]

            first_table.remove_guests(first_table_people)
            second_table.remove_guests(second_table_people)
            first_table.add_guests(second_table_people)
            second_table.add_guests(first_table_people)

    @staticmethod
    def _pick_at_least_one_from_table(relationships, table):
        first_person = random.sample(table.guests(), 1)[0]
        return get_tens(table.guests(), relationships, first_person)

    def _pick_exactly_n_from_table(self, relationships, table, number):
        groups = itertools.groupby(table.guests(), partial(get_tens, table.guests(), relationships))
        group_lens = {group:len(group) for group in groups}

    def restore_state(self, tables_states):
        """
        :param tables_states: tuple of tuples of guest names.
        :return:
        """
        self._tables = set()
        try:
            for table_state in tables_states:
                table = Table(max_size=len(table_state))
                for guest in table_state:
                    table.add_guest(guest)
                self._tables.add(table)
        except Exception:
            raise TableException('Failed to restore state!')


