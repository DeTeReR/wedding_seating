class Table(object):
    def __init__(self, max_size):
        self._max_size = max_size
        self._guests = set()

    def add_guest(self, guest):
        if guest in self._guests:
            raise