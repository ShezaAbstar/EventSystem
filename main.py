from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum


app = FastAPI()

class EventStatus(BaseModel):
    Available: 1
    Unavailable : 2
    Cancelled : 3
    Postponed: 4

class Event(BaseModel):
    EventId : int
    EventName : str
    EventStartDate: str

class Customer(BaseModel):
    CustomerId : int
    CustomerName : str
    EmailId : str

# class EventUpdate(BaseModel):
    EventDetail : Event
    EventStatusDetail : EventStatus 
    DiscountPricePercent : int
    Price : float

class Booking(BaseModel):
    BookingId : int
    CustomerDetail :Customer
    EventDetail : Event
    NumberOfGuests : int
    TotalPrice : float
    # DiscountedPrice: float
    # EventUpdateDetail : EventUpdate

    # def CalculateDiscountedPrice(self): 
    #     DiscountedPrice = self.TotalPrice * (self.EventUpdateDetail.DiscountPricePercent /100)
    #     return DiscountedPrice

class BookedEvents(BaseModel):
    bookings:list[Booking]

items = []

@app.get("/")
def root():
    return {"EventPackages:Discounts"}

@app.post("/items")
def create_item(item :str):
    items.append(item)
    return items

@app.get("/items/{item_id}")
def get_item(item_id :int) -> str:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code = 404, detail="Item can't be found")


@app.get("/items")  
def list_items(limit: int = 10):
    return items[0:limit]

@app.get("/items")
def get_items() -> items:
    return items