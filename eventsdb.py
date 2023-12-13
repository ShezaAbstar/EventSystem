import sqlite3
from sqlite3 import Error



def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()




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

def create_event(conn, event):
    """
    Create a new event into the events table
    :param conn:
    :param event:
    :return: event id
    """
    sql = ''' INSERT INTO events(Name, StartDate, EndDate, Family_price, Adult_price, Child_price)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, event)
    conn.commit()
    return cur.lastrowid


def main():
    database = r"C:\sqlite\db\bookingevents.db"

    # create a database connection
    conn = create_db_connection(database)
    with conn:
        # create a new Event
        event = ('Feeding the elephants', '2015-01-01', '2015-01-30', 30.00, 20.00, 10.00);
        event_id = create_event(conn, event)


if __name__ == '__main__':
    main()

