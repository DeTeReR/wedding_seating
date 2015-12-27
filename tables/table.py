class Table(object):
    def __init__(self, max_size):
        self._max_size = max_size
        self._guests = set()

    def add_guest(self, guest):
        if guest in self._guests:
            raise Exception('%s is already on this table!', guest.name)
        if len(self._guests) >= self._max_size:
            raise Exception('Too many guests on this table, can\'t add %s.', guest.name)
        self._guests.add(guest)

    def remove_guest(self, guest):
        if guest not in self._guests:
            raise Exception('Can\'t remove %s from table, they aren\'t sitting here.', guest.name)
        self._guests.remove(guest)

    def guests(self):
        return self._guests

    def state(self):
        return self._guests[:]