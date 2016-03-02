import argparse


def get_parser():
    parser = argparse.ArgumentParser(description='Wedding Seating simluation')
    parser.add_argument(
        '-g',
        '--guest_file_name',
        type=str,
        default='relationship.csv',
        help='file containing guest information.')
    parser.add_argument(
        '-ts',
        '--table_size',
        type=int,
        default=10,
        help='Maximum number of people that can sit on an ordinary table.')
    parser.add_argument(
        '-i',
        '--iterations',
        type=int,
        default=1000,
        help='Number of iterations for the annealing.')
    parser.add_argument(
        '-b',
        '--high_score_filename',
        type=str,
        default='temp',
        help='Name of file in which best result found so far is kept.')
    return parser
