from wedding import Wedding
import logging


def main():
    wedding = Wedding(
        guest_file_name='relationship.csv',
        table_size=10,
                      )
    x = wedding.do_seating(
        high_score_filename='high_score',
        iterations=100000,
    )
    print(x)

if '__main__' == __name__:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    main()
