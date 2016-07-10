import itertools
import logging
import math
import random
from functools import partial

from tables.score import Score
from tables.table import Table, TableException
from tables.wedding_state import WeddingState

LOGGER = logging.getLogger(__name__)


def get_tens(people, relationships, the_one):
    return frozenset([person for person in people if relationships[frozenset([the_one, person])] == 10] + [the_one])


def _pick_exactly_n_from_table(relationships, table, number):
        groups = set(key for key, value in itertools.groupby(
            table.guests(),
            partial(get_tens, table.guests(), relationships))
        )
        #group_lens = {group: len(group) for group in groups}
        options = []
        for i in range(1, number + 1):
            options.extend([c for c in itertools.combinations(groups, i) if sum(len(g) for g in c) == number])
        if not options:
            return None
        return set(list(itertools.chain(*random.sample(options, 1)[0])))


def _pick_at_least_n_from_table(relationships, table, number):
    population = table.guests()
    chosen = set()
    while len(chosen) < number:
        person = random.sample(population=population - chosen, k=1)[0]
        chosen.update(get_tens(table.guests(), relationships, person))
    return chosen


class TablePlan(object):
    def __init__(self, table_size=10, guest_count=130):
        num_tables = math.ceil(guest_count/table_size)
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
        return sum((table.score(relationships=relationships) for table in self._tables), Score())

    def state(self):
        return WeddingState([table.state() for table in self._tables])

    def swap(self, relationships, count=1):
        for i in range(count):
            first_table, second_table = sorted(random.sample(self._tables, 2), key=lambda t: len(t.guests()))
            for number_to_pick in range(1, min(len(first_table.guests()), len(second_table.guests())) + 1):
                first_table_people = _pick_at_least_n_from_table(relationships, first_table, number_to_pick)
                second_table_people = _pick_exactly_n_from_table(relationships, second_table, len(first_table_people))
                if second_table_people:
                    break
            if not second_table_people:
                LOGGER.warning(
                    'Couldn\'t do the swap:%s from:\n%s\nto:\n%s',
                    first_table_people,
                    first_table,
                    second_table)
                continue

            first_table.remove_guests(first_table_people)
            second_table.remove_guests(second_table_people)
            first_table.add_guests(second_table_people)
            second_table.add_guests(first_table_people)

    def restore_state(self, wedding_state):
        """
        :param wedding_state: tuple of tuples of guest names.
        :return:
        """
        self._tables = set()
        try:
            for table_state in wedding_state:
                table = Table(max_size=len(table_state))
                for guest in table_state:
                    table.add_guest(guest)
                self._tables.add(table)
        except Exception:
            raise TableException('Failed to restore state!')


