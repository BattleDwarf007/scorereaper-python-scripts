import time

from scorereaper_platform.cr_log import get_logger
from scorereaper_platform.database import create_db_client, get_scrutineer_scan, write_scrutineer_score_to_db, \
    refresh_points_score_table

log = get_logger("scrutineer_score")


def calculate_age_score(input_age):
    score = 0

    if input_age > 1986:
        score = 0
    elif input_age == 1985:
        score = 10
    elif 1980 <= input_age <= 1984:
        score = 15
    elif 1975 <= input_age <= 1979:
        score = 17
    elif 1970 <= input_age <= 1974:
        score = 20
    elif 1960 <= input_age <= 1969:
        score = 22
    elif input_age <= 1959:
        score = 25

    return score


def calculate_value_score(input_value):
    score = 0

    if input_value > 30000:
        score = 0
    elif input_value == 30000:
        score = 5
    elif 25000 <= input_value <= 29999:
        score = 15
    elif 20000 <= input_value <= 24999:
        score = 20
    elif input_value <= 20000:
        score = 25

    return score


def calculate_engine_score(input_size):
    score = 0

    if input_size > 5000:
        score = 0
    elif 1000 <= input_size <= 1200:
        score = 25
    elif 1201 <= input_size <= 1400:
        score = 22
    elif 1401 <= input_size <= 2000:
        score = 20
    elif 2001 <= input_size <= 2500:
        score = 17
    elif 2501 <= input_size <= 3000:
        score = 15
    elif 3001 <= input_size <= 4000:
        score = 10
    elif 4001 <= input_size <= 5000:
        score = 7

    return score


def main():
    while True:
        startTime = time.time()
        new_db_conn = create_db_client()

        log.info("Starting...")

        all_scrutineer_scans = get_scrutineer_scan(new_db_conn)

        for i in all_scrutineer_scans:
            log.info(f"Processing car: {i['id']}...")
            # Get the scrutineering result
            age = calculate_age_score(i['score_year'])
            engine = calculate_engine_score(i['score_engine_size'])
            value = calculate_value_score(i['score_value'])
            total = age + engine + value + i['score_accurate'] + i['score_spirit'] + i['score_veteran']
            # # Do the upload to the correct table
            write_scrutineer_score_to_db(new_db_conn, i['id'], total)
            print(f'car:{i}/Total:{total}')

        refresh_points_score_table(new_db_conn)

        # Run every 15 minutes

        endTime = time.time() - startTime
        log.info(f"Processing took {endTime} seconds to complete")
        log.info(f"Processing complete, sleeping for 15 minutes")
        time.sleep(60 * 15)


if __name__ == '__main__':
    main()
