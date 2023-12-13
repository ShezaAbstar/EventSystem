from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

def create_db_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def getevents():
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    database = r"C:/sqlite/db/bookingevents.db"

    # create a database connection
    conn = create_db_connection(database)

    cur = conn.cursor()
    cur.execute("SELECT Name, eventDesc FROM Events")

    events = cur.fetchall()

    return events

@app.route("/") 
def index(): # You could name this whatever you want.
  eventsinfo = getevents()
  return render_template("index.html", eventsData = eventsinfo)


@app.route("/makebooking")
def makebooking():
  return render_template('makebooking.html')

@app.route("/signup")
def signup():
  return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
