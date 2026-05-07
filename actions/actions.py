from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import csv
import re
from datetime import datetime

# Load Parcel Data
PARCEL_DB = {}
with open('parcel_data.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        PARCEL_DB[row['tracking_number']] = row

# Load Bus Routes
BUS_SCHEDULES = {}
with open('bus_routes.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        BUS_SCHEDULES[(row['source'], row['destination'])] = {
            "times": row['times'],
            "price": f"Rs.{row['price']}",
            "duration": row['duration']
        }

# Load Cities Data
CITIES = {}
with open('cities.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        CITIES[row['city'].lower()] = row
        CITIES[row['code'].lower()] = row

city_map = {
    "lhr": "lahore", "lahore": "lahore", "lhore": "lahore",
    "khi": "karachi", "karachi": "karachi",
    "isl": "islamabad", "islamabad": "islamabad",
    "pesh": "peshawar", "peshawar": "peshawar",
    "mul": "multan", "multan": "multan",
    "qta": "quetta", "quetta": "quetta",
}

class ActionTrackParcel(Action):
    def name(self) -> str:
        return "action_track_parcel"
    
    def run(self, dispatcher, tracker, domain):
        text = tracker.latest_message.get("text", "")
        match = re.search(r'PK\d{5}', text.upper())
        
        if match:
            tracking = match.group()
            parcel = PARCEL_DB.get(tracking)
            
            if parcel:
                message = f"📦 PARCEL STATUS: {tracking}\n\n"
                message += f"✅ Status: {parcel['status']}\n"
                message += f"📍 Location: {parcel['location']}\n"
                message += f"📅 Expected Delivery: {parcel['estimated_delivery']}\n"
                message += f"⚖️ Weight: {parcel['weight_kg']} kg\n"
                message += f"💰 Price: Rs.{parcel['price']}\n"
                message += f"🚚 From: {parcel['sender_city']} → To: {parcel['receiver_city']}"
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text=f"❌ No parcel found with tracking number {tracking}")
        else:
            dispatcher.utter_message(text="Please provide tracking number (e.g., PK10001)")
        return []

class ActionBookParcel(Action):
    def name(self) -> str:
        return "action_book_parcel"
    
    def run(self, dispatcher, tracker, domain):
        # Get slots
        sender = tracker.get_slot("sender_city")
        receiver = tracker.get_slot("receiver_city")
        weight = tracker.get_slot("weight")
        
        if not sender or not receiver:
            message = "📦 PARCEL BOOKING GUIDE\n\n"
            message += "To book a parcel, provide:\n"
            message += "1️⃣ Sender city\n"
            message += "2️⃣ Receiver city\n"
            message += "3️⃣ Weight (kg)\n\n"
            message += "Example: 'Book parcel from Lahore to Karachi weighing 5kg'"
            dispatcher.utter_message(text=message)
        else:
            # Calculate price
            base_price = CITIES.get(sender.lower(), {}).get('base_price_parcel', 200)
            total_price = base_price * (int(weight) if weight else 1)
            
            message = f"✅ PARCEL BOOKING CONFIRMED!\n\n"
            message += f"📤 From: {sender}\n"
            message += f"📥 To: {receiver}\n"
            message += f"⚖️ Weight: {weight} kg\n"
            message += f"💰 Total Price: Rs.{total_price}\n\n"
            message += f"Tracking number will be sent via SMS. Thank you!"
            dispatcher.utter_message(text=message)
        return []

class ActionShowBusSchedule(Action):
    def name(self) -> str:
        return "action_show_bus_schedule"
    
    def run(self, dispatcher, tracker, domain):
        text = tracker.latest_message.get("text", "").lower()
        
        src, dst = None, None
        for word in text.split():
            if word in city_map:
                if src is None:
                    src = city_map[word]
                else:
                    dst = city_map[word]
        
        if src and dst:
            schedule = BUS_SCHEDULES.get((src, dst))
            if schedule:
                message = f"🚌 BUS SCHEDULE: {src.title()} → {dst.title()}\n\n"
                message += f"🕐 Departures: {schedule['times']}\n"
                message += f"💰 Fare: {schedule['price']}\n"
                message += f"⏱️ Duration: {schedule['duration']}\n"
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text=f"❌ No route from {src.title()} to {dst.title()}")
        else:
            dispatcher.utter_message(text="Say: Lahore to Karachi bus")
        return []

class ActionLLMFallback(Action):
    def name(self) -> str:
        return "action_llm_fallback"
    
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Sorry, I didn't understand. Try: 'track PK10001' or 'book parcel'")
        return []
