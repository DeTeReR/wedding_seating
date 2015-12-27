from collections import namedtuple, defaultdict

Guest = namedtuple('Guest', ['name', 'sex'])


class GuestList(object):
    def __init__(self, guest_list_file):
        self._guests = dict()
        self._relationships = defaultdict(lambda: 0)
        for line in guest_list_file:
            pass

    def __len__(self):
        return len(self._guests)

    def relationship_weight(self, person_one, person_two):
        return self._relationships[frozenset([person_one, person_two])]

    def relationships(self):
        return self._relationships

    def guests(self):
        return self._guests.values()

    def guest(self, name):
        return self._guests.get(name)

    @staticmethod
    def create_relationship(a, b, weight):
        for this, other in [(a, b), (b, a)]:
            if any(other in r for r in ._relationships):
                raise Exception('%s already has relationship with %s ')
        relationship = Relationship(self, other, weight)