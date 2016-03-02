from collections import namedtuple, defaultdict


class Guest(namedtuple('Guest', ['name'])):
    def __repr__(self):
        return str(self.name)



class GuestList(object):
    _INPUT_GRID_START_ROW = 2
    _INPUT_GRID_START_COL = 0

    def __init__(self, guest_list_file):
        self._guests = dict()
        self._relationships = defaultdict(lambda: 0)
        input_grid = [l.split(',') for l in open(guest_list_file)]
        names = [n for n in input_grid[self._INPUT_GRID_START_ROW] if n]
        self._guests = dict((n, Guest(name=n)) for n in names)
        for i in range(len(names)):
            row = i + 1 + self._INPUT_GRID_START_ROW
            assert names[i].strip() == input_grid[row][0].strip()
            for j in range(i):
                col = j + 1
                weight = input_grid[row][col]
                if weight:
                    pair = frozenset([self._guests[names[i]], self._guests[names[j]]])
                    assert pair not in self._relationships
                    self._relationships[pair] = int(weight)

    def __len__(self):
        return len(self._guests)

    def relationship_weight(self, person_one, person_two):
        return self._relationships[frozenset([person_one, person_two])]

    def relationships(self):
        return self._relationships

    def guests(self):
        return list(self._guests.values())

    def guest(self, name):
        return self._guests.get(name)
