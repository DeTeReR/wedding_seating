import argparse
from guests.guest_list import GuestList
from tables.table_plan import TablePlan


class Wedding(object):
    def __init__(self, guest_file, table_size=10):
        self._guests = GuestList(guest_file)
        self._table_plan = TablePlan(table_size=table_size, guest_count=len(self._guests))

    def seat_guests(self):
        self._table_plan.seat_guests(self._guests)

    def run_annealing(self):
        pass

def Parser():
    parser = argparse.ArgumentParser(description='Wedding Seating simluation')
    parser.add_argument()
    parser.add_argument()

def main():
    kwargs = vars(Parser().parse_args())
    wedding = Wedding(**kwargs)
    wedding.seat_guests()
    plan = wedding.run_annealing(**kwargs)
    print(plan)

if '__main__' == __name__:
    main()


