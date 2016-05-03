import atexit
import datetime
import logging
import os
import pickle
from math import exp
from pprint import pprint
from random import random

import math

from guest_list import GuestList
from parser import get_parser
from result import Result
from tables.table import TableException
from tables.table_plan import TablePlan

_LOGGER = logging.getLogger(__name__)


class Wedding(object):
    def __init__(self, guest_file_name=None, table_size=10, **_):
        self._guest_list = GuestList(guest_file_name)
        self._table_plan = TablePlan(table_size=table_size, guest_count=len(self._guest_list))
        self._table_plan.seat_guests(self._guest_list.guests())
        self._best_result = Result(state=self._table_plan.state())

    def __str__(self):
        return 'Wedding(_table_plan=%s, _guest_list=%s)' % (self._table_plan, self._guest_list)

    @staticmethod
    def _load_previous_result(high_score_filename):
        previous_result = None
        if high_score_filename:
            if not os.path.exists(high_score_filename):
                os.mknod(high_score_filename)
            elif os.stat(high_score_filename).st_size:
                with open(high_score_filename, 'rb') as high_score_file:
                    try:
                        previous_result = pickle.load(high_score_file)
                    except TypeError:
                        _LOGGER.exception('Can\'t unpickle %s', high_score_filename)
                    except UnicodeDecodeError:
                        _LOGGER.exception('Can\'t unpickle %s', high_score_filename)
        if previous_result:
            _LOGGER.info('Loaded previous result from %s with score %s.',
                         high_score_filename,
                         previous_result.score)
        return previous_result

    @classmethod
    def _save_new_best_result(cls, high_score_filename, new_result):
        previous_result = cls._load_previous_result(high_score_filename)
        if previous_result is None or previous_result.score < new_result.score:
            with open(high_score_filename, 'wb') as high_score_file:
                pickle.dump(new_result, high_score_file)
            _LOGGER.info('New best score:%s\nsaved in %s', new_result.score, high_score_filename)

    def do_seating(self, iterations=1000, high_score_filename=None, **_):
        previous_result = self._load_previous_result(high_score_filename)
        self._best_result = previous_result if previous_result else self._best_result
        atexit.register(self._save_new_best_result, **dict(high_score_filename=high_score_filename,
                                                           new_result=self._best_result))
        self._run_annealing(iterations=iterations)
        self._save_new_best_result(high_score_filename=high_score_filename,
                                   new_result=self._best_result)
        return self._best_result

    def _run_annealing(self, iterations):
        if self._best_result:
            try:
                self._table_plan.restore_state(self._best_result.state)
            except TableException:
                _LOGGER.exception('Failed to load state %s.', self._best_result.state)

        current_result = Result()
        for iteration in range(iterations):
            if iteration % math.ceil(iterations / 100) == 0:
                _LOGGER.info('Have done %s iterations.\nCurrent score is %s, best score is %s',
                             iteration, current_result.score, self._best_result.score)

            current_result.state = self._table_plan.state()
            current_result.score = self._table_plan.score(self._guest_list.relationships())
            self._table_plan.swap(relationships=self._guest_list.relationships())
            new_score = self._table_plan.score(self._guest_list.relationships())

            if new_score > self._best_result.score:
                _update_result(self._best_result, new_score, self._table_plan.state())

            if new_score >= current_result.score:
                _update_result(current_result, new_score, self._table_plan.state())

            else:
                score_difference_multiplier = self._best_result.score.difference_multiplier(new_score)
                proportion_done = 1 - ((iterations - iteration) / iterations)
                if random() < score_difference_multiplier * exp(-proportion_done * 5) * 0.01:
                    _update_result(current_result, new_score, self._table_plan.state())
                else:
                    self._table_plan.restore_state(current_result.state)

        _LOGGER.info('Took %s steps in total\nscore:%s\nstate:%s',
                     iterations, self._best_result.score, self._best_result.state)

        return self._best_result


def _update_result(result, new_score, new_state):
    result.score = new_score
    result.timestamp = datetime.datetime.utcnow()
    result.state = new_state


def main():
    kwargs = vars(get_parser().parse_args())
    wedding = Wedding(**kwargs)
    pprint(wedding.do_seating(**kwargs))



if '__main__' == __name__:
    logging.basicConfig(level=logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(stream_handler)
    main()
