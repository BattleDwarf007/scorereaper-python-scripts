import time

from scorereaper_platform.cr_log import get_logger
from scorereaper_platform.database import create_db_client, get_points_scan, write_points_to_db, \
    refresh_laps_score_table, get_car_list, refresh_points_score_table

log = get_logger("consolidations")

LOCATIONS = [
    "activity1",
    "activity2",
    "activity3",
]


def main():
    while True:
        startTime = time.time()
        new_db_conn = create_db_client()
        log.info("Starting...")
        all_cars = get_car_list(new_db_conn)

        for location in LOCATIONS:
            log.info(f"Processing location: {location}...")
            for car in all_cars:
                points_entry = get_points_scan(new_db_conn, car, location)
                scans = []
                for i in points_entry:
                    scans.append(i['points'])
                total = sum(scans)
                # Do the upload to the correct table
                write_points_to_db(new_db_conn, location, car, total)

        refresh_points_score_table(new_db_conn)

        new_db_conn.close()

        endTime = time.time() - startTime
        log.info(f"Processing took {endTime} seconds to complete")
        # Run every 15 minutes
        log.info(f"Processing complete, sleeping for 15 minutes")
        time.sleep(60 * 15)


if __name__ == '__main__':
    main()
