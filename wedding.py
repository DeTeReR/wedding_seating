import argparse

from guest_list import GuestList
from tables.table_plan import TablePlan
import logging
_LOGGER = logging.getLogger(__name__)


class Wedding(object):
    def __init__(self, guest_file, table_size=10, *_, **__):
        self._guest_list = GuestList(guest_file)
        self._table_plan = TablePlan(table_size=table_size, guest_count=len(self._guest_list))

    def seat_guests(self):
        self._table_plan.seat_guests(self._guest_list.guests())

    def run_annealing(self, swaps_to_try=1, *_, **__):
        count = 0
        repetition_count = 0
        score = 0
        while repetition_count < 100:
            count += 1
            if count % 10000:
                _LOGGER.info('Have done %s iterations. Current score is %s', count, score)
            state = self._table_plan.state()
            self._table_plan.swap(count=swaps_to_try)
            new_score = self._table_plan.score(self._guest_list.relationships())
            if new_score > score:
                score = new_score
                repetition_count = 0
            else:
                repetition_count += 1
                if new_score < score:
                    self._table_plan.restore_state(state)
                    #TODO!!!!

        return None


def get_parser():
    parser = argparse.ArgumentParser(description='Wedding Seating simluation')
    parser.add_argument()
    parser.add_argument()


def main():
    kwargs = vars(get_parser().parse_args())
    wedding = Wedding(**kwargs)
    wedding.seat_guests()
    plan = wedding.run_annealing(**kwargs)
    print(plan)


if '__main__' == __name__:
    logging.basicConfig()
    main()
