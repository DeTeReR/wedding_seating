class GuestList(object):

    @staticmethod
    def create_relationship(a, b, weight):
        for this, other in [(a, b), (b, a)]:
            if any(other in r for r in ._relationships):
                raise Exception('%s already has relationship with %s ')
        relationship = Relationship(self, other, weight)