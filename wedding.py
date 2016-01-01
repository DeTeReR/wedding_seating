import argparse
import datetime
import os
import pickle
from guest_list import GuestList
from parser import get_parser
from result import Result
from tables.table import TableException
from tables.table_plan import TablePlan
import atexit
import logging

_LOGGER = logging.getLogger(__name__)


class Wedding(object):
    def __init__(self, guest_file_name=None, table_size=10, **_):
        self._guest_list = GuestList(guest_file_name)
        self._table_plan = TablePlan(table_size=table_size, guest_count=len(self._guest_list))
        self._table_plan.seat_guests(self._guest_list.guests())
        self._best_result = Result()

    def __str__(self):
        return 'Wedding(_table_plan=%s, _guest_list=%s)' % (self._table_plan, self._guest_list)

    @staticmethod
    def _load_previous_best_score(high_score_filename):
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
        previous_result = cls._load_previous_best_score(high_score_filename)
        if previous_result is None or previous_result.score < new_result.score:
            with open(high_score_filename, 'wb') as high_score_file:
                pickle.dump(new_result, high_score_file)
            _LOGGER.info('New best score:%s\nsaved in %s', new_result.score, high_score_filename)

    # def _save_state_on_exit(self, high_score_filename=None, previous_result=None):
    #     current_state = self._table_plan.state()
    #     new_result = Result(state=current_state,
    #                         score=self._table_plan.score(self._guest_list.relationships()))
    #
    #     _LOGGER.info('Saving State before closing: file:%s, score:%s', high_score_filename, new_result.score)
    #     import pdb
    #     pdb.set_trace()
    #     self._save_new_best_result(high_score_filename=high_score_filename,
    #                                previous_result=previous_result,
    #                                new_result=new_result)

    def do_seating(self, high_score_filename=None, **kwargs):
        previous_result = self._load_previous_best_score(high_score_filename)
        self._best_result = previous_result if previous_result else Result(state=self._table_plan.state())
        # atexit.register(self._save_state_on_exit, **dict(high_score_filename=high_score_filename,
        #                                                  previous_result=previous_result))
        atexit.register(self._save_new_best_result, **dict(high_score_filename=high_score_filename,
                                                           new_result=self._best_result))
        new_result = self._run_all_annealing(**kwargs)
        self._save_new_best_result(high_score_filename=high_score_filename,
                                   new_result=new_result)
        return new_result

    def _run_all_annealing(self, **kwargs):
        result = self._run_annealing()
        return self._run_annealing(**kwargs)

    def _run_annealing(self, swaps_to_annealing=1, failures_allowed=200, **_):
        repetition_count = count = 0
        if self._best_result:
            try:
                self._table_plan.restore_state(self._best_result.state)
            except TableException:
                _LOGGER.exception('Failed to load state %s.', self._best_result.state)

        while repetition_count < failures_allowed:
            count += 1
            if count % 10000 == 0:
                _LOGGER.info('Have done %s iterations.\nCurrent score is %s',
                             count, self._best_result.score)

            self._best_result.state = self._table_plan.state()
            self._table_plan.swap(count=swaps_to_annealing)
            new_score = self._table_plan.score(self._guest_list.relationships())

            if new_score > self._best_result.score:
                self._best_result.score = new_score
                self._best_result.timestamp = datetime.datetime.utcnow()
                self._best_result.state = self._table_plan.state()
                repetition_count = 0

            elif new_score == self._best_result.score:
                self._best_result.state = self._table_plan.state()
                repetition_count += 1

            elif new_score < self._best_result.score:
                self._table_plan.restore_state(self._best_result.state)
                repetition_count += 1

        _LOGGER.info('Took %s steps in total\nscore:%s\nstate:%s',
                     count, self._best_result.score, self._best_result.state)
        return self._best_result


def main():
    kwargs = vars(get_parser().parse_args())
    wedding = Wedding(**kwargs)
    plan = wedding.do_seating(**kwargs)
    from pprint import pprint as pp
    #pp(plan.state)


if '__main__' == __name__:
    logging.basicConfig(level=logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(stream_handler)
    main()
