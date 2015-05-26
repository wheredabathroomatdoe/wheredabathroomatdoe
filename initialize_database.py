import psycopg2
from constants import *

conn = psycopg2.connect("dbname='%s' user='%s'" % (DB_NAME, DB_USER))
c = conn.cursor()

# To create the database:
#sudo -u postgres psql -c "CREATE DATABASE users"
# To delete the database:
#sudo -u postgres psql -c "DROP DATABASE users"
# To list databases:
# >> psql
# <db>=# \l
# To connect to a database:
# >> psql
# <db>=# \connect <dbname>
# To list tables:
# >> psql
# <dbname>=# \dt

#show table names
c.execute("SELECT relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
tables_list =  c.fetchall()
print tables_list

if ("users",) in tables_list:
    try:
        #next two lines show previous contents in table Users
        c.execute("SELECT * FROM Users")
        print c.fetchall()
        #delete everything in Users table
        c.execute("DROP TABLE Users")
    except Exception, e:
        print "Error displaying contents of Users database: %s" % e
if ("places",) in tables_list:
    try:
        #next two lines show previous contents in table Places
        c.execute("SELECT * FROM Places")
        print c.fetchall()
        #delete everything in Places table
        c.execute("DROP TABLE Places")
    except Exception, e:
        print "Error displaying contents of Places database: %s" % e

if ("reviews",) in tables_list:
    try:
        #next two lines show previous contents in table Reviews
        c.execute("SELECT * FROM Reviews")
        print c.fetchall()
        #delete everything in Reviews table
        c.execute("DROP TABLE Reviews")
    except Exception, e:
        print "Error displaying contents of Reviews database: %s" % e

# Create new Users, Places, and Reviews tables
c.execute("CREATE TABLE Users (Email TEXT, Password TEXT, Phone TEXT)")
c.execute("""CREATE TABLE Places (ID INT, Name TEXT, LocationX DOUBLE PRECISION,
          LocationY DOUBLE PRECISION, Favorites INT, Finder TEXT)""")
c.execute("CREATE TABLE Reviews (ID INT, Username TEXT, Rating INT, Review TEXT)")
conn.commit()
