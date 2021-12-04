import time

import numpy as np
import pandas as pd

from scorereaper_platform.cr_log import get_logger
from scorereaper_platform.database import create_db_client, get_laps_scans, write_rank_to_db, get_car_list, \
    refresh_laps_score_table

log = get_logger("rank_calcs")

LOCATIONS = [
    "activity1",
    "activity2",
    "activity3",
]


def perform_rank_calculation(location, all_cars, new_db_conn):
    log.info(f"Processing location: {location}...")
    rank_list = []
    for car in all_cars:
        scanned_lap_times = []
        entries = get_laps_scans(new_db_conn, car, location)
        if len(entries) > 0:
            for i in entries:
                if i["lap_time"] > 0:
                    scanned_lap_times.append(i["lap_time"])

            rank_list.append(min(scanned_lap_times))
        else:
            rank_list.append(np.NAN)

    df = pd.DataFrame(data={
        "car": all_cars,
        "lap": rank_list
    })

    df['default_rank'] = df['lap'].rank(method='dense', na_option='keep')

    return df


def score_calculation_with_upload(location, new_db_conn, rankData):
    log.info(f"Writing rank data for {location}...")
    rankData = rankData.replace({np.nan: None})
    for i, r in rankData.iterrows():
        if r['default_rank'] is not None:
            if r['default_rank'] == 1:
                score = 250
            elif 1 < r['default_rank'] <= 250:
                score = 249 - r['default_rank']
            else:
                score = 0

            if r['default_rank'] > 0:
                write_rank_to_db(new_db_conn, location, r['car'], r['lap'], r['default_rank'], score)


def main():
    while True:
        startTime = time.time()
        new_db_conn = create_db_client()
        log.info("Starting...")
        all_cars = get_car_list(new_db_conn)
        for location in LOCATIONS:
            rankData = perform_rank_calculation(location,all_cars, new_db_conn)

            score_calculation_with_upload(location,new_db_conn, rankData)

        refresh_laps_score_table(new_db_conn)

        new_db_conn.close()

        endTime = time.time() - startTime
        log.info(f"Processing took {endTime} seconds to complete")

        # Run every 15 minutes
        log.info(f"Processing complete, sleeping for 15 minutes")
        time.sleep(60 * 15)


if __name__ == '__main__':
    main()
