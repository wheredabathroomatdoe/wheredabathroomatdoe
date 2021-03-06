import psycopg2, psycopg2.extras
import dbhelper
import validate
import uuid
import users_dbhelper as usersdb
from constants import *
from utils import *

def add_place(place_type, location_x, location_y, finder, description, conn=None):
    global ID_PLACE
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return "Database Error"
    c = conn.cursor()
    try:
        c.execute("""SELECT 1 FROM Places WHERE PlaceType=%s AND LocationX=%s AND
                LocationY=%s LIMIT 1""",
                 (place_type, location_x, location_y))
        exists = c.fetchone()
        if not exists:
            puid = dbhelper.generate_id(ID_PLACE)
            if not puid[0]:
                return puid[1]
            c.execute("INSERT INTO Places VALUES(%s, %s, %s, %s, %s, 0, %s, %s)",
                      (puid[1], puid[1], place_type, location_x, location_y,
                          usersdb.get_user_id(finder), description))
            conn.commit()
            return "Location added to map"
        else:
            return "Location already exists"
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()

def remove_place(place_type, location_x, location_y, conn=None):
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return "Database Error"
    c = conn.cursor()
    try:
        c.execute("""DELETE FROM Places WHERE PlaceType = %s AND LocationX = %s AND LocationY = %s""", (place_type, location_x, location_y))
        conn.commit()
        return "Location removed from map"
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()

def remove_place_by_id(place_id, conn=None):
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return "Database Error"
    c = conn.cursor()
    try:
        c.execute("""DELETE FROM Places WHERE PlaceId = %s""", (place_id,))
        conn.commit()
        return "Location removed"
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()

def get_place_finder(place_id, conn=None):
    global ID_PLACE
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return "Database Error"
    c = conn.cursor()
    try:
        c.execute("SELECT Finder FROM Places WHERE PlaceId=%s LIMIT 1",
                 (place_id,))
        results = c.fetchone()
        return results[0] if results else None
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()

def get_places(conn=None):
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return "Database Error"
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM PLACES")
        conn.commit()
        return dictionarify(c.fetchall())
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()

def get_place_id(place_type, location_x, location_y, conn=None):
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return "Database Error"
    c = conn.cursor()
    try:
        c.execute("""SELECT * FROM Places WHERE PlaceType = %s AND
                abs(LocationX - %s) < 0.0000000000001 AND 
                abs(LocationY - %s) < 0.0000000000001 LIMIT 1""",
                (place_type, location_x, location_y))
        return c.fetchone()[0]
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()

def get_place_type(pid, conn=None):
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return "Database Error"
    c = conn.cursor()
    try:
        c.execute("SELECT PlaceType FROM Places WHERE ID = %s LIMIT 1", (pid,))
        result = c.fetchone()
        return result[0] if result else None
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()

# TODO merge this with get_place_location_y because stop being stupid
def get_place_location_x(pid, conn=None):
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return "Database Error"
    c = conn.cursor()
    try:
        c.execute("SELECT LocationX FROM Places WHERE ID = %s LIMIT 1", (pid,))
        result = c.fetchone()
        return result[0] if result else None
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()

def get_place_location_y(pid, conn=None):
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return "Database Error"
    c = conn.cursor()
    try:
        c.execute("SELECT LocationY FROM Places WHERE ID = %s LIMIT 1", (pid,))
        result = c.fetchone()
        return result[0] if result else None
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()

def get_place_description(pid, conn=None):
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return "Database Error"
    c = conn.cursor()
    try:
        c.execute("SELECT Description FROM Places WHERE PlaceID = %s LIMIT 1",
                                                                        (pid,))
        result = c.fetchone()
        if result and result[0]:
            return result[0]
        else:
            return ''
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()

def update_place_description(pid, description, conn=None):
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return "Database Error"
    c = conn.cursor()
    try:
        c.execute("UPDATE Places SET Description = %s WHERE PlaceID = %s",
                                                       (description, pid))
        conn.commit()
        return "Successfully updated description"
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()

def dictionarify(places_list):
    ans = []
    for place in places_list:
        place_dict = {
            "ID": str(place[0]),
            "type": place[2],
            "position": [place[3], place[4]],
            "finder": str(place[6]),
            "description": str(place[7]),
        }
        ans.append(place_dict)
    return ans

def get_local_places(location_x, location_y, radius, conn=None):
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return "Database Error"
    c = conn.cursor()
    try:
        c.execute("""SELECT * FROM PLACES WHERE abs(LocationX-%s) <= %s AND
        abs(LocationY-%s) <= %s AND (LocationX-%s)^2 +
        (LocationY-%s)^2 <= %s""",
        (location_x, radius, location_y, radius, location_x, location_y,
            radius**2))
        conn.commit()
        return dictionarify(c.fetchall())
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()

def add_place_report(reporter_id, reported_id, reason, conn=None):
    global ID_REPORTS_PLACES, PLACE_REPORT_LIMIT
    ruid = dbhelper.generate_id(ID_REPORTS_PLACES)
    if not ruid[0]:
        return (False, "UUID error")
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return (False, "Database Error")
    c = conn.cursor()
    try:
        c.execute("""INSERT INTO ReportsPlaces (ID, ReportID, ReporterId,
            ReportedId, Reason)  VALUES (%s, %s, %s, %s, %s)""",
                (ruid[1], ruid[1], reporter_id, reported_id, reason))
        conn.commit()
        if get_num_reports_for_place(reported_id) >= PLACE_REPORT_LIMIT:
            remove_place_by_id(reported_id)
            # TODO perhaps, add an intermediary disabled state, rather than
            # automatically removing the place
        return (True, "Place report successful")
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()

def remove_place_report(reporter_id, reported_id, conn=None):
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return (False, "Database Error")
    c = conn.cursor()
    try:
        c.execute("""REMOVE FROM ReportsPlaces WHERE ReporterId = %s AND
            ReportedId = %s """, (reporter_id, reported_id))
        conn.commit()
        return (True, "Place report removal successful")
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()

def is_place_reported_by(reporter_id, reported_id, conn=None):
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return (False, "Database Error")
    c = conn.cursor()
    try:
        c.execute("""SELECT 1 FROM ReportsPlaces WHERE ReporterId = %s AND
            ReportedId = %s LIMIT 1 """, (reporter_id, reported_id))
        return c.fetchone()
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()

def can_place_be_reported(reporter_id, reported_id, conn=None):
    return get_place_finder(reported_id, conn) != reporter_id and\
            not is_place_reported_by(reporter_id, reported_id, conn)

def get_num_reports_for_place(reported_id, conn=None):
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return (False, "Database Error")
    c = conn.cursor()
    try:
        c.execute("""SELECT 1 FROM ReportsPlaces WHERE ReportedId = %s""",
                (reported_id,))
        return len(c.fetchall())
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()

def created_place(user_id, place_id, conn=None):
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return (False, "Database Error")
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM Places WHERE Finder=%s AND ID=%s LIMIT 1", (user_id, place_id))
        exists = c.fetchone()
        if exists:
            return True
        else:
            return False
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()

def calc_rating(place_id, conn=None):
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return (False, "Database Error")
    c = conn.cursor()
    try:
        c.execute("SELECT Rating FROM Reviews WHERE PlacesId=%s", (place_id,))
        ratings = c.fetchall()
        total = 0
        for rating in ratings:
            total += rating[0]
        avg = float(total / len(ratings))
        c.execute("UPDATE Places SET Rating=%s WHERE ID=%s", (avg, place_id))
        conn.commit()
        return avg
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()

def get_place_rating(place_id, conn=None):
    persist_conn = True
    if not conn:
        conn = dbhelper.connect()
        persist_conn = False
    if conn == None:
        return (False, "Database Error")
    c = conn.cursor()
    try:
        c.execute("SELECT Rating FROM Places WHERE ID=%s LIMIT 1", (place_id,))
        rating = c.fetchone()
        if rating and rating[0]:
            return "%.2f" % rating[0]
        else:
            return "No rating"
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn and not persist_conn:
            conn.close()
