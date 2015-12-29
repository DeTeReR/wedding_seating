from wedding import Wedding
import logging


def main():
    wedding = Wedding(guest_file_name='relationship.csv')
    x = wedding.do_seating(high_score_filename='high_score')
    print(x)

if '__main__' == __name__:
    logging.basicConfig()
    main()
