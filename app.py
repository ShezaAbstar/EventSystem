from flask import Flask, render_template, request, session
import sqlite3
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "27eduCBA09"
app.permanent_session_lifetime = timedelta(minutes=5)

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

def getEventDetails(eventId):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    connection = sqlite3.connect("C:/sqlite/db/bookingevents.db")
    cursor = connection.cursor()

    # Execute your SQL query (replace 'your_table' and 'your_column' accordingly)
    cursor.execute("SELECT Name, EventDesc, startdate, enddate, family_price, adult_price, child_price, imagename, Event_id FROM Events where Event_id = ? ", eventId)
    event = cursor.fetchall()
    # print(data.count)
    # Close the connection
    cursor.close()
    connection.close()

    return event

def UpdateBooking(event_id, guest_count, customer_name, email):
    connection = sqlite3.connect("C:/sqlite/db/bookingevents.db")
    cursor = connection.cursor()

    # Execute your SQL query (replace 'your_table' and 'your_column' accordingly)
    cursor.execute("insert into Customer (Name, EmailId, Password) values (?, ?, ?) ", (customer_name, email, "Test"))
    customer_id = cursor.lastrowid
    print(f'Customer id : {cursor.lastrowid}')
    connection.commit()
    cursor.close()
    
    cursor1 = connection.cursor()
    cursor1.execute("insert into Booking (Customer_Id, EventId, EventDate, TotalPrice, NumberofGuest) values (?, ?, ?, ?, ?) ", (customer_id, event_id, "2023/12/22", "45.00", guest_count))
    bookingReference = cursor1.lastrowid
    print(f'Booking Ref : {cursor1.lastrowid}  ref: {bookingReference}')
    connection.commit()
    cursor1.close()
    print('Record inserted succesfully')

    connection.close()

    return bookingReference

def getevents():
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    connection = sqlite3.connect("C:/sqlite/db/bookingevents.db")
    cursor = connection.cursor()

    # Execute your SQL query (replace 'your_table' and 'your_column' accordingly)
    cursor.execute("SELECT Name, EventDesc, startdate, enddate, family_price, adult_price, child_price, imagename, Event_id FROM Events")
    events = cursor.fetchall()
    # print(data.count)
    # Close the connection
    cursor.close()
    connection.close()

    return events

def  GetLoginDetails(uname, psw):
    connection = sqlite3.connect("C:/sqlite/db/bookingevents.db")
    cursor = connection.cursor()
    cursor.execute("select Customer_Id, Name, EmailId FROM Customer where EmailId = ? and password = ?", (uname, psw))
    loginDetails = cursor.fetchall()
    print(f'Login details: {loginDetails}')
    if len(loginDetails) == 0:
       login = None
    else:
        for login_s in loginDetails:
            login = login_s
        
    
    
    # Close the connection
    cursor.close()
    connection.close()

    return login

def  GetBookingDetails(bookingId):
    connection = sqlite3.connect("C:/sqlite/db/bookingevents.db")
    cursor = connection.cursor()
    #print(f'Booking Ref : {bookingId} ')
    # Execute your SQL query (replace 'your_table' and 'your_column' accordingly)
    # cursor.execute("select BookingId, c.Name, c.EmailId, e.Name [EventName], b.NumberOfGuest from Booking b Join Customer c on c.Customer_id = b.Customer_id Join Events e on e.Event_id = b.EventId where BookingId = ? ", BookingId)
    cursor.execute("select BookingId, c.Name, c.EmailId, e.Name [EventName], b.NumberOfGuest from Booking b Join Customer c on c.Customer_id = b.Customer_id Join Events e on e.Event_id = b.EventId where BookingId = ? ", (bookingId,))
    bookingDetails = cursor.fetchall()
    #print(f'Booking details: {bookingDetails}')
    # Close the connection
    cursor.close()
    connection.close()

    return bookingDetails

@app.route("/") 
def index(): # You could name this whatever you want.
  eventsinfo = getevents()
  num_rows = len(eventsinfo)
  images = (
     ("monkey", "monkeyevent"),
     ("elephants", "tigerevent"),
     ("tiger", "tigerevent")
  )
  return render_template("index.html", data = eventsinfo, num_rows=num_rows, images=images)

@app.route("/makebooking", methods=('GET', 'POST'))
def makebooking():
  if request.method == 'GET':
     event_id = request.args.get('event_id')
     session['event_id'] = event_id
     print(f'Event id : {event_id} ')
     customer_id = session.get('customer_id')
     print(f'customer_id : {customer_id} ')
     if session.get('customer_id') is None:
        return render_template("login.html", event = event_id )
     elif request.args.get('event_id', None):
        eventDetail = getEventDetails(event_id)   #getEventDetails(request.args['event_id'])
        print(f'eventDetail : {eventDetail} ')
        return render_template('makebooking.html', eventData=eventDetail)
  if request.method == 'POST':
     event_id = request.form.get("event_id")
     event_name= request.form.get("name")
     guest_count = request.form.get("Guest_count")
     customer_name = request.form.get("Customer_name")
     email = request.form.get("Email")
     bookingId = UpdateBooking(event_id, guest_count, customer_name, email)
     #print(f'After insert Booking Ref : {bookingId} ')
     bookingDetails = GetBookingDetails(bookingId)

     return render_template('confirmbooking.html', bookingData=bookingDetails)
  
@app.route("/login", methods=('GET', 'POST'))
def login():
  print(f'login : ')
  if request.method == 'POST':
     username = request.values.get("uname")
     password= request.values.get("psw")
     #Customer_id = session.get["customer_id"]
     #print(f'username : {username} psw: {passsword}')
     event_id = session.get('event_id')
     loginDetails = GetLoginDetails(username, password)
     if loginDetails is not None:
        session["customer_id"] = loginDetails[0]
        print(f'customer_id : {loginDetails[0]}')
        eventDetail = getEventDetails(event_id)
        print(f'login : {loginDetails} eventDetail : {eventDetail}')
        return render_template('makebooking.html', eventData=eventDetail )
     else:
        return render_template('login.html', event = event_id)
  
 
if __name__ == '__main__':
    app.run(debug=True)