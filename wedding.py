import argparse
from collections import namedtuple
import datetime
import os
import pickle
from guest_list import GuestList
from tables.table import TableException
from tables.table_plan import TablePlan
import atexit
import logging

_LOGGER = logging.getLogger(__name__)


Result = namedtuple('Result', ['score', 'timestamp', 'state'])


class Wedding(object):
    def __init__(self, guest_file_name=None, table_size=10, **_):
        self._guest_list = GuestList(guest_file_name)
        self._table_plan = TablePlan(table_size=table_size, guest_count=len(self._guest_list))
        self._table_plan.seat_guests(self._guest_list.guests())

    def _previous_best_score(self, high_score_filename):
        if high_score_filename:
            previous_result = None
            if not os.path.exists(high_score_filename):
                os.mknod(high_score_filename)
            else:
                with open(high_score_filename, 'rb') as high_score_file:
                    try:
                        previous_result = pickle.load(high_score_file)
                    except TypeError:
                        logging.exception('Can\'t unpickle %s', high_score_filename)
                    except UnicodeDecodeError:
                        logging.exception('Can\'t unpickle %s', high_score_filename)
        return previous_result

    def _save_new_best_result(self, high_score_filename, previous_result, new_result):
        if previous_result is None or previous_result.score < new_result.score:
            with open(high_score_filename, 'wb') as high_score_file:
                pickle.dump(new_result, high_score_file)
            _LOGGER.info('New best score:%s\nsaved in %s', new_result.score, high_score_filename)

    def _save_state_on_exit(self, high_score_filename=None, previous_result=None):
        current_state = self._table_plan.state()
        new_result = Result(state=current_state,
                               score=self._table_plan.score(self._guest_list.relationships()),
                               timestamp=datetime.datetime.utcnow())
        _LOGGER.debug('Saving State before closing: %s, %s, %s', self, high_score_filename, previous_result)
        self._save_new_best_result(high_score_filename=high_score_filename,
                                   previous_result=previous_result,
                                   new_result=new_result)

    def do_seating(self, high_score_filename=None, **kwargs):

        previous_result = self._previous_best_score(high_score_filename)
        atexit.register(self._save_state_on_exit, **dict(high_score_filename=high_score_filename,
                                                   previous_result=previous_result))


        new_result = self._run_all_annealing(previous_result=previous_result, **kwargs)
        self._save_new_best_result(high_score_filename=high_score_filename,
                                   previous_result=previous_result,
                                   new_result=new_result)

        return new_result

    def __str__(self):
        return 'Wedding(_table_plan=%s, _guest_list=%s)' % (self._table_plan, self._guest_list)

    def _run_all_annealing(self, previous_result=None, **kwargs):
        result = self._run_annealing(previous_result=previous_result)
        return self._run_annealing(previous_result=result, **kwargs)

    def _run_annealing(self, previous_result=None, swaps_to_annealing=1, failures_allowed=200, **_):
        score = repetition_count = count = 0
        if previous_result:
            try:
                self._table_plan.restore_state(previous_result.state)
                score = previous_result.score
            except TableException:
                _LOGGER.exception('Failed to load state %s.', previous_result.state)
                pass
        while repetition_count < failures_allowed:
            count += 1
            if count % 10000 == 0:
                _LOGGER.info('Have done %s iterations.\nCurrent score is %s\nState is ?', count, score)
            state = self._table_plan.state()

            self._table_plan.swap(count=swaps_to_annealing)
            new_score = self._table_plan.score(self._guest_list.relationships())

            if new_score > score:
                score = new_score
                repetition_count = 0
                state = self._table_plan.state()
            elif new_score == score:
                    state = self._table_plan.state()
                    repetition_count += 1
            elif new_score < score:
                self._table_plan.restore_state(state)
                repetition_count += 1

        logging.debug('Took %s steps in total\nscore:%s\nstate:%s', count, score, state)
        return Result(score=score, state=state, timestamp=datetime.datetime.utcnow())


def get_parser():
    parser = argparse.ArgumentParser(description='Wedding Seating simluation')
    parser.add_argument('-g',
                        '--guest_file_name',
                        type=str,
                        help='file containing guest information.')
    parser.add_argument('-ts',
                        '--table_size',
                        type=int,
                        help='Maximum number of people that can sit on an ordinary table.')
    parser.add_argument('-s',
                        '--swaps_to_annealing',
                        type=int,
                        help='Number of swaps to take place for each annealing step.')
    parser.add_argument('-f',
                        '--failures_allowed',
                        type=int,
                        help='Number of annealing steps which do not improve the score that we are allowed to take.')
    parser.add_argument('-b',
                        '--high_score_filename',
                        type=str,
                        help='Name of file in which best result found so far is kept.')


    return parser


def main():
    kwargs = vars(get_parser().parse_args())
    wedding = Wedding(**kwargs)
    plan = wedding.do_seating(**kwargs)
    from pprint import pprint as pp
    #pp(plan.state)


if '__main__' == __name__:
    logging.basicConfig(level=logging.INFO)
    main()
