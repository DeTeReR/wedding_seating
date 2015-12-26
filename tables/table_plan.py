class TablePlan(object):
    def __init__(self, table_size=10, guest_count=130):
        self._tables = set(t for t in guest_count/table_size)

    def seat_guests(self, guests):
        raise NotImplementedError()

    def score(self):
        raise NotImplementedError()

    def state(self):
        raise NotImplementedError()

    def swap(self):
        raise NotImplementedError()

    def restore_state(self, state):
        raise NotImplementedError()