import psycopg2
import sys
from flask import flash, session
from constants import *
import validate

def auth(type, email, password, phone=None):
    conn = None
    try:
        conn = psycopg2.connect("dbname='%s' user='%s'" % (DB_NAME, DB_USER))
        c = conn.cursor()
        if type=="register":
            c.execute("SELECT 1 FROM Users WHERE Email = %s", (email,))
            if c.fetchall() == []:
                c.execute("INSERT INTO Users VALUES(%s, %s, %s)",
                          (email, validate.generate_password_hash(password),
                           phone))
                conn.commit()
                print "Registration successful"
                flash("Registration successful")
            else:
                print "Username is taken"
                flash("Username is taken")
        elif type=="login":
            print c.execute("""SELECT * FROM Users WHERE Email = %s""",
                            (email,))
            results = c.fetchall()
            success = False
            if results != []:
                if validate.check_password(results[0][1], password):
                    print "Login successful"
                    flash("Login successful")
                    session['email'] = email
                    success = True
            if not success:
                print "Incorrect login information"
                flash("Incorrect login information")
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn:
            conn.close()

def addPlace(name, locationX, locationY, finder):
    conn = None
    try:
        conn = psycopg2.connect("dbname='%s' user='%s'" % (DB_NAME, DB_USER))
        c = conn.cursor()
        #remember to change the first 0 into a random int
        c.execute("SELECT * FROM Places WHERE Name=%s AND LocationX=%s AND LocationY=%s", (name, locationX, locationY))
        exists = c.fetchall()
        if exists == []:
            c.execute("INSERT INTO Places VALUES(%s, %s, %s, %s, 0, %s)",
                  (0, name, locationX, locationY, finder))
            print "Location added to map"
            flash("Location added to map")
        else:
            print "Location already exists"
            flash ("Location already exists")
        conn.commit()
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn:
            conn.close()

def removePlace(name, locationX, locationY):
    conn = None
    try:
        conn = psycopg2.connect("dbname='%s' user='%s'" % (DB_NAME, DB_USER))
        c = conn.cursor()
        c.execute("""DELETE FROM Places WHERE Name = '%s' AND LocationX = %s AND
                  LocationY = %s""", (name, locationX, locationY))
        conn.commit()
        print "Location removed from map"
        flash("Location removed from map")
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn:
            conn.close()

def getPlaces():
    conn = None
    try:
        conn = psycopg2.connect("dbname='%s' user='%s'" % (DB_NAME, DB_USER))
        c = conn.cursor()
        c.execute("SELECT * FROM PLACES")
        return dictionarify(c.fetchall())
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn:
            conn.close()

def dictionarify(placesList):
    print "placeslist: " + str(placesList)
    ans = []
    for place in placesList:
        placeID = place[0]
        placeType = place[1]
        print "placeType: " + str(placeType)
        placePosition = [place[2], place[3]]
        print "placePosition: " + str(placePosition)
        placeFinder = place[4]
        placeDict = {
            "ID": placeID,
            "type": placeType,
            "position": placePosition,
            "finder": placeFinder
        }
        ans.append(placeDict)
    return ans

def getLocalPlaces(locationX, locationY, radius):
    conn = None
    try:
        conn = psycopg2.connect("dbname='%s' user='%s'" % (DB_NAME, DB_USER))
        c = conn.cursor()
        c.execute("""SELECT * FROM PLACES WHERE LocationX-%s <= %s AND
                  LocationY-%s <= %s""" % (locationX, radius, locationY, radius))
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if conn:
            conn.close()
