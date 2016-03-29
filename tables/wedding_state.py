class WeddingState(object):
    def __init__(self, table_states):
        self._table_states = table_states

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self._table_states))

    def __str__(self):
        return 'WeddingState(%s)' % '\n'.join([str(table_state) for table_state in self._table_states])

    def __iter__(self):
        for table_state in self._table_states:
            yield table_state