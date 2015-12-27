import itertools
import random
from tables.table import Table


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

    def seat_guests(self, guests):
        raise NotImplementedError()

    def score(self, relationships):
        score = 0
        for table in self._tables:
            for pair_of_people in itertools.combinations(table.guests(), 2):
                score += relationships[frozenset(pair_of_people)]
        return score

    def state(self):
        return (table.state() for table in self._tables)

    def swap(self, count=1):
        for i in range(count):
            first_table, second_table = random.sample(self._tables, 2)
            first_person = random.choice(first_table.guests())
            second_person = random.choice(second_table.guests())
            first_table.remove_guest(first_person)
            second_table.remove_guest(second_person)
            first_table.add_guest(second_person)
            second_table.add_guest(first_person)

    def restore_state(self, tables_states):
        """
        :param tables_states: tuple of tuples of guest names.
        :return:
        """
        self._tables = set()
        for table_state in tables_states:
            table = Table(max_size=len(table_state))
            for guest in table_state:
                table.add_guest(guest)
            self._tables.add(table)
