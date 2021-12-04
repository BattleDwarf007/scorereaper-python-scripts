import pymysql.cursors

from scorereaper_platform.cr_log import get_logger

log = get_logger(__name__)


def create_db_client():
    try:
        db_connection = pymysql.connect(
            user="admin",
            password="admin",
            host="localhost",
            port=3306,
            database="db"

        )
    except pymysql.Error as e:
        log.error(f"Error connecting to MariaDB Platform: {e}")

    return db_connection


def create_db_client_asroot():
    global db_connection
    try:
        db_connection = pymysql.connect(
            user="nonadmin",
            password="nonadmin",
            host="localhost",
            port=3306,
            database="db"

        )
    except pymysql.Error as e:
        log.error(f"Error connecting to MariaDB Platform: {e}")

    return db_connection


def get_car_list(db):
    try:
        result_list = []
        dbcursor = db.cursor(pymysql.cursors.DictCursor)
        sql = "call get_cars_list()"
        dbcursor.execute(sql)
        result = dbcursor.fetchall()

        for record in result:
            result_list.append(record['id'])

    except pymysql.Error as e:
        log.error(f"Error getting list of all cars: {e}")

    return result_list


def refresh_laps_score_table(db):
    try:
        dbcursor = db.cursor()
        sql = "call consolidate_laps_scores()"
        dbcursor.execute(sql)

    except pymysql.Error as e:
        log.error(f"Error calling procesdure consolidate_laps_scores(): {e}")


def refresh_points_score_table(db):
    try:
        dbcursor = db.cursor()
        sql = "call consolidate_points_scores()"
        dbcursor.execute(sql)

    except pymysql.Error as e:
        log.error(f"Error calling procesdure consolidate_laps_scores(): {e}")


def get_laps_scans(db, car, location):
    try:
        result_list = []
        dbcursor = db.cursor(pymysql.cursors.DictCursor)
        sql = "call get_lap_scans_for_car_and_location(%s,%s)"
        dbcursor.execute(sql, (car, location))
        result_list = dbcursor.fetchall()

    except pymysql.Error as e:
        log.error(f"Error getting lap scans for {car} in location {location}: {e}")

    return result_list


def get_points_scan(db, car, location):
    try:
        result_list = []
        dbcursor = db.cursor(pymysql.cursors.DictCursor)
        sql = "call get_points_scans_for_car_and_location(%s,%s)"
        dbcursor.execute(sql, (car, location))
        result_list = dbcursor.fetchall()

    except pymysql.Error as e:
        log.error(f"Error getting lap scans for {car} in location {location}: {e}")

    return result_list


def get_scrutineer_scan(db):
    try:
        result_list = []
        dbcursor = db.cursor(pymysql.cursors.DictCursor)
        sql = "call get_all_scrutineer_scan_results()"
        dbcursor.execute(sql)
        result_list = dbcursor.fetchall()

    except pymysql.Error as e:
        log.error(f"Error getting scans: {e}")

    return result_list


def write_rank_to_db(db, location, car, lap, rank, score):
    try:
        dbcursor = db.cursor()
        sql = f"call save_{location}_rank(%s,%s,%s,%s)"
        dbcursor.execute(sql, (car, lap, rank, score))
        db.commit()
    except pymysql.Error as e:
        log.error(f"Error saving data to database: {e}")


def write_points_to_db(db, location, car, score):
    try:
        dbcursor = db.cursor()
        sql = f"call job_save_{location}_score(%s,%s)"
        dbcursor.execute(sql, (car, score))
        db.commit()
    except pymysql.Error as e:
        log.error(f"Error saving data to database: {e}")


def write_scrutineer_score_to_db(db, car, score):
    try:
        dbcursor = db.cursor()
        sql = "call job_save_scrutineer_score(%s,%s)"
        dbcursor.execute(sql, (car, score))
        db.commit()
    except pymysql.Error as e:
        log.error(f"Error saving data to database: {e}")


def run_all_score_consolidation(db, car):
    try:
        dbcursor = db.cursor()
        sql = "call run_consolidate_scores(%s)"
        dbcursor.execute(sql, car)
        db.commit()
    except pymysql.Error as e:
        log.error(f"Error running proc: {e}")
