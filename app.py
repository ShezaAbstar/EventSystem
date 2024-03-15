from flask import Flask, render_template, request, session
import sqlite3
from datetime import timedelta
import re
import json

app = Flask(__name__)
app.secret_key = "27eduCBA09"
app.permanent_session_lifetime = timedelta(minutes=10)

EventUpdates = '[{"EventId": 1, "EventName": "Monkey Madness", "DiscountPrice": 10.4}, {"EventId": 2,"EventName": "Feeding the Elephants","DiscountPrice": 22.0},{"EventId": 3,"EventName": "Chatting the Tiger","DiscountPrice": 16.9},{"EventId": 4,"EventName": "Dolphin Diving","DiscountPrice": 12.3}]'

class Customer():
    def __init__(self, name, emailID):
        self.CustomerName = name 
        self.EmailId = emailID

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
    event = cursor.fetchone()
    # print(data.count)
    # Close the connection
    cursor.close()
    connection.close()

    return event

def UpdateBooking(event_id, guest_count, customer_id):
    connection = sqlite3.connect("C:/sqlite/db/bookingevents.db")
    cursor = connection.cursor()

    eventDetail = getEventDetails(event_id)
    bookingCost = float(eventDetail[5]) * float(guest_count)
    cursor1 = connection.cursor()
    cursor1.execute("insert into Booking (Customer_Id, EventId, EventDate, TotalPrice, NumberofGuest) values (?, ?, ?, ?, ?) ", (customer_id, event_id, "2023/12/22", bookingCost, guest_count))
    bookingReference = cursor1.lastrowid
    print(f'Booking Ref : {cursor1.lastrowid}  ref: {bookingReference}')
    connection.commit()
    cursor1.close()
    print('Record inserted succesfully')

    connection.close()

    return bookingReference

def UpdateCustomer(customer_name, email, password):
    connection = sqlite3.connect("C:/sqlite/db/bookingevents.db")
    cursor = connection.cursor()

    # Execute your SQL query (replace 'your_table' and 'your_column' accordingly)
    cursor.execute("insert into Customer (Name, EmailId, Password) values (?, ?, ?) ", (customer_name, email, password))
    customer_id = cursor.lastrowid
    print(f'Customer id : {cursor.lastrowid}')
    connection.commit()
    cursor.close()

    connection.close()

    return customer_id

# load the json response for all the discounted events 
def getdiscounts() :
   eventDiscounts = json.loads(EventUpdates) 
   for events in eventDiscounts:    
      print(f'discounts: { events["EventId"]}')
   return eventDiscounts

# fetch the prices from the database 
def comparePrices(events, eventDiscounts):
   for i, event in enumerate(events):
      for eventdisc in  eventDiscounts:
         if event[8] == eventdisc["EventId"]:
            if event[5] > eventdisc["DiscountPrice"]:
                eventdisc["Flag"] =  '1'
            else:
                eventdisc["Flag"] =  '0'
            #event[i].extend(val)
            print (f'event id: {event[8]} == {eventdisc["EventId"]}, disc: {event[5]} > {eventdisc["DiscountPrice"]}, discounted : {i} : {eventdisc["Flag"]}')

   print(f'discounts: { eventDiscounts}')
   return eventDiscounts

def GetComparePricesOfEevents(events, eventDiscounts):
   List_of_events = []
   for i, event in enumerate(events):
      for eventdisc in  eventDiscounts:
         if event[8] == eventdisc["EventId"]:
            if eventdisc["Flag"] == "1":
                event_with_disc = (eventdisc["EventName"], event[1], event[2], event[3], event[4], event[5], event[6], event[7], eventdisc["EventId"], eventdisc["DiscountPrice"], eventdisc["Flag"])
                print (f'event id: {event[8]} == {eventdisc["EventId"]}, disc: {event[5]} > {eventdisc["DiscountPrice"]}, discounted : {i} : {eventdisc["Flag"]}')
            else:
                event_with_disc = (eventdisc["EventName"], event[1], event[2], event[3], event[4], event[5], event[6], event[7], eventdisc["EventId"], eventdisc["DiscountPrice"], "0")
            List_of_events.append(event_with_disc) 
   return List_of_events
        

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
    print(f'events {events}')
    # Close the connection
    cursor.close()
    connection.close()

    return events

def  GetLoginDetails(uname, psw):
    connection = sqlite3.connect("C:/sqlite/db/bookingevents.db")
    cursor = connection.cursor()
    cursor.execute("select Customer_Id, Name, EmailId FROM Customer where EmailId = ? and password = ?", (uname, psw))
    loginDetails = cursor.fetchone()
    print(f'Login details: {loginDetails}') 
    
    # Close the connection
    cursor.close()
    connection.close()

    return loginDetails

def  GetCustomerDetails(customerId):
    connection = sqlite3.connect("C:/sqlite/db/bookingevents.db")
    cursor = connection.cursor()
    #print(f'Booking Ref : {bookingId} ')
    # Execute your SQL query (replace 'your_table' and 'your_column' accordingly)
    # cursor.execute("select BookingId, c.Name, c.EmailId, e.Name [EventName], b.NumberOfGuest from Booking b Join Customer c on c.Customer_id = b.Customer_id Join Events e on e.Event_id = b.EventId where BookingId = ? ", BookingId)
    cursor.execute("select Customer_Id, Name, EmailId FROM Customer c where Customer_Id = ? ", (customerId,))
    customerDetail = cursor.fetchone()
    # Close the connection
    cursor.close()
    connection.close()

    return customerDetail

def  GetBookingDetails(bookingId):
    connection = sqlite3.connect("C:/sqlite/db/bookingevents.db")
    cursor = connection.cursor()
    #print(f'Booking Ref : {bookingId} ')
    # Execute your SQL query (replace 'your_table' and 'your_column' accordingly)
    # cursor.execute("select BookingId, c.Name, c.EmailId, e.Name [EventName], b.NumberOfGuest from Booking b Join Customer c on c.Customer_id = b.Customer_id Join Events e on e.Event_id = b.EventId where BookingId = ? ", BookingId)
    cursor.execute("select BookingId, c.Name, c.EmailId, e.Name [EventName], b.NumberOfGuest, b.TotalPrice from Booking b Join Customer c on c.Customer_id = b.Customer_id Join Events e on e.Event_id = b.EventId where BookingId = ? ", (bookingId,))
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
  event_discounts = getdiscounts()
  updated_event_discounts = comparePrices(eventsinfo, event_discounts)
  event_prices = GetComparePricesOfEevents(eventsinfo, updated_event_discounts)
  print(f'event_prices: {event_prices}')
  print(f'eventsinfo: {eventsinfo}')
  images = (
     ("monkey", "monkeyevent"),
     ("elephants", "tigerevent"),
     ("tiger", "tigerevent")
  )
  return render_template("index.html", data = event_prices, num_rows=num_rows, images=images)

@app.route("/makebooking", methods=('GET', 'POST'))
def makebooking():
  if request.method == 'GET':
     event_id = request.args.get('event_id')
     session['event_id'] = event_id
     print(f'Event id : {event_id} ')
     customer_id = session.get('customer_id')
     print(f'customer_id : {customer_id} ')
     eventDetail = getEventDetails(event_id)   #getEventDetails(request.args['event_id'])
     customer_details = GetCustomerDetails(customer_id)
     session["customer_id"] = customer_id
     print(f'customer data : {customer_details} event_details : {eventDetail}')
     if session.get('customer_id') is None:
        return render_template("login.html", event = eventDetail, error = 0 )
     elif request.args.get('event_id', None):
        return render_template('makebooking.html', eventData=eventDetail, customer = customer_details)
  if request.method == 'POST':
     #Checking for session values for event and customer are stored 
     event_id = session.get('event_id')
     if event_id is None:
        return render_template('index.html')
     eventDetail = getEventDetails(event_id)
     customer_id = session.get('customer_id')
     if customer_id is None:
        return render_template('login.html', event = eventDetail, error = 0)
     guest_count = request.form.get("Guest_count")
     #customer_name = request.form.get("Customer_name")
     #email = request.form.get("Email")
     bookingId = UpdateBooking(event_id, guest_count, customer_id)
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
     eventDetail = getEventDetails(event_id)
     print(f'Login details: {loginDetails} event details: {eventDetail}')
     if loginDetails is not None:
        customer_id = loginDetails[0]
        session["customer_id"] = customer_id
        customer_details = GetCustomerDetails(customer_id)
        return render_template('makebooking.html', eventData=eventDetail, customer = customer_details)
     else:
        print(f'login failed : {loginDetails} event_id : {event_id}')
        return render_template('login.html', event = eventDetail, error = 1)
     
@app.route("/register", methods=('GET','POST'))
def register():
   event_id = session.get('event_id')
   print(f'event id : {event_id}')
   eventDetail = getEventDetails(event_id)
   if request.method == 'POST':
    customer_name = request.form.get("Customer_name")
    patternemail = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    email = request.form.get("Email")
    #customer = Customer(customer_name, email)
    #patternpassword = "^.*(?=.{8,})(?=.*/s\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$"
    patternpassword ="^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$"
    password = request.form.get("Password")
    result = re.match(patternpassword, password)
    result1 = re.match(patternemail, email)
    print(f'result : {result}, password : {password} email : {email}')
    # if re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*?[#@$])[\w\d@#$]{3,12}$", password):
    #     print ("match pass")
    # else:
    #     print ("Not Match pass")
    # if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'", email):
    #     print ("match email")
    # else:
    #     print ("Not Match email")
    if (result) and (result1):        
        customer_id = UpdateCustomer(customer_name, email, password)
        customer_details = GetCustomerDetails(customer_id)
        session["customer_id"] = customer_id
        print(f'customer data : {customer_details} event_details : {eventDetail}')
        return render_template('makebooking.html', eventData=eventDetail, customer = customer_details )
    else:
        #print(f'customer name : {customer.CustomerName}, email : {customer.EmailId}')
        if result is None:
            errorValue = 1
        if result1 is None:
            errorValue = 2
        if result is None and result1 is None:
            errorValue = 3
        return render_template('register.html', event=eventDetail, customerName = customer_name, customerEmail = email, error =  errorValue )
   if request.method == 'GET':
        #customer = Customer("","")
        customer_name = ""
        email = ""
        return render_template('register.html', event=eventDetail, customerName = customer_name, customerEmail = email, error = 0 )
 
if __name__ == '__main__':
    app.run(debug=True)