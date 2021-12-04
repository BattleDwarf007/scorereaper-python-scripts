import time

from scorereaper_platform.cr_log import get_logger
from scorereaper_platform.database import create_db_client, get_car_list, run_all_score_consolidation, \
    create_db_client_asroot

log = get_logger("score_consolidations")


def main():
    while True:
        startTime = time.time()
        new_db_conn = create_db_client_asroot()
        log.info("Starting...")
        all_cars = get_car_list(new_db_conn)

        for car in all_cars:
            run_all_score_consolidation(new_db_conn, car)

        new_db_conn.close()

        endTime = time.time() - startTime
        log.info(f"Processing took {endTime} seconds to complete")
        # Run every 15 minutes
        log.info(f"Processing complete, sleeping for 15 minutes")
        time.sleep(60 * 15)


if __name__ == '__main__':
    main()
