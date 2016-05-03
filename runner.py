import logging

from wedding import Wedding


def main():
    wedding = Wedding(
        guest_file_name='relationship_2016_5_3.csv',
        table_size=10,
                      )
    x = wedding.do_seating(
        high_score_filename='high_score_2016_5_3',
        iterations=3000000,
    )
    print(x)

if '__main__' == __name__:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    main()
