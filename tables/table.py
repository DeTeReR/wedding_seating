import copy


class TableException(Exception):
    pass


class Table(object):
    def __init__(self, max_size):
        self._seat_count = max_size
        self._guests = set()

    def __str__(self):
        return 'Table(_max_size=%s, _guests=%s)' % (self._seat_count, self._guests)

    def add_guest(self, guest):
        if guest in self._guests:
            raise TableException('%s is already on this table!', guest.name)
        if len(self._guests) >= self._seat_count:
            raise TableException('Too many guests on this table, can\'t add %s.', guest.name)
        self._guests.add(guest)

    def remove_guest(self, guest):
        if guest not in self._guests:
            raise TableException('Can\'t remove %s from table, they aren\'t sitting here.', guest.name)
        self._guests.remove(guest)

    def guests(self):
        return self._guests

    def state(self):
        return copy.copy(self._guests)

    def seat_count(self):
        return self._seat_count
