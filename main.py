from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class EventStatus(BaseModel):
    Available: 1
    Unavailable : 2
    Cancelled : 3
    Postponed: 4

    class Config:
        arbitrary_types_allowed = True

class Customer(BaseModel):
    CustomerId : int
    CustomerName : str
    EmailId : str 

    class Config:
        arbitrary_types_allowed = True

class EventUpdate(BaseModel):
    EventId : int
    EventName : str
    DiscountPrice : float
    
    class Config:
        arbitrary_types_allowed = True


    
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

class Booking(BaseModel):
    BookingId : int
    CustomerDetail :Customer
    EventId : int
    NumberOfGuests : int
    TotalPrice : float
    # DiscountedPrice: float
    # EventUpdateDetail : EventUpdate

    # def CalculateDiscountedPrice(self): 
    #     DiscountedPrice = self.TotalPrice * (self.EventUpdateDetail.DiscountPricePercent /100)
    #     return DiscountedPrice
    class Config:
        arbitrary_types_allowed = True

class BookedEvents(BaseModel):
    bookings:list[Booking]
    class Config:
        arbitrary_types_allowed = True

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

@app.get("/events")  
async def get_events() -> list[EventUpdate]:
     return [
         EventUpdate(EventId=1, EventName="Monkey Madness", DiscountPrice=10.4), 
          EventUpdate(EventId=2, EventName="Feeding the Elephants", DiscountPrice=15.3),  
           EventUpdate(EventId=3, EventName="Chatting the Tiger", DiscountPrice=16.9),
            EventUpdate(EventId=4, EventName="Dolphin Diving", DiscountPrice=12.3)          
     ]

@app.get("/list/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]

@app.get("/items")
def get_items() -> items:
    return items