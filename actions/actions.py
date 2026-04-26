from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import re
import google.generativeai as genai


genai.configure(api_key="AIzaSyDeIc5KEj-B4AkUSdLqoZZG7R1NIX4EToI")
model = genai.GenerativeModel('gemini-pro')

def translate_response(user_message, english_response):
    """User ki language pe response convert karo"""
    prompt = f"""
User message: "{user_message}"
English response: "{english_response}"

Instructions:
- If user wrote in English → Keep as is
- If user wrote in Roman Urdu (e.g., "salam", "kesy ho", "lahore se karachi") → Convert response to Roman Urdu
- If user wrote in Urdu script → Convert response to Urdu script
- Keep same meaning, emojis, and formatting
- Reply with ONLY translated response
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return english_response

class ActionShowBusSchedule(Action):
    def name(self): return "action_show_bus_schedule"
    
    def run(self, dispatcher, tracker, domain):
        user_msg = tracker.latest_message.get("text", "").lower()
        
        # Extract cities
        cities = {
            "lahore": "Lahore", "lhr": "Lahore", "لاہور": "Lahore",
            "karachi": "Karachi", "khi": "Karachi", "کراچی": "Karachi",
            "islamabad": "Islamabad", "isl": "Islamabad", "اسلام آباد": "Islamabad",
            "peshawar": "Peshawar", "pesh": "Peshawar", "پشاور": "Peshawar",
        }
        
        # Urdu city names
        urdu_cities = {
            "lahore": "لاہور", "karachi": "کراچی", 
            "islamabad": "اسلام آباد", "peshawar": "پشاور"
        }
        
        src = None
        dst = None
        
        for word in user_msg.split():
            if word in cities:
                if src is None:
                    src = cities[word]
                else:
                    dst = cities[word]
        
        if src and dst:
            schedule = f"🚌 BUS SCHEDULE: {src} → {dst}\n🕐 7AM, 10AM, 1PM, 4PM, 8PM, 11PM\n💰 Fare: Rs.1500-2500"
            urdu_schedule = f"🚌 بس ٹائم: {urdu_cities.get(src.lower(), src)} → {urdu_cities.get(dst.lower(), dst)}\n🕐 صبح 7, 10, دوپہر 1, شام 4, رات 8, 11 بجے\n💰 کرایہ: 1500-2500 روپے"
            
            # Check if user wrote in Urdu
            if any(u'\u0600' <= c <= u'\u06FF' for c in user_msg):
                dispatcher.utter_message(text=urdu_schedule)
            else:
                dispatcher.utter_message(text=translate_response(user_msg, schedule))
        else:
            msg = "Please tell: Lahore to Karachi bus / براہ کرم بتائیں: لاہور سے کراچی بس"
            dispatcher.utter_message(text=msg)
        
        return []

class ActionTrackParcel(Action):
    def name(self): return "action_track_parcel"
    
    def run(self, dispatcher, tracker, domain):
        user_msg = tracker.latest_message.get("text", "")
        match = re.search(r'pk\d{3,10}', user_msg.lower())
        
        if match:
            tracking = match.group().upper()
            english = f"📦 PARCEL: {tracking}\n✅ Status: In Transit\n📍 Location: Lahore Hub"
            urdu = f"📦 پارسل: {tracking}\n✅ حیثیت: راستے میں\n📍 مقام: لاہور ہب"
            
            if any(u'\u0600' <= c <= u'\u06FF' for c in user_msg):
                dispatcher.utter_message(text=urdu)
            else:
                dispatcher.utter_message(text=translate_response(user_msg, english))
        else:
            dispatcher.utter_message(text="Please provide tracking number like PK12345 / براہ کرم ٹریکنگ نمبر دیں PK12345")
        return []

class ActionContactAdmin(Action):
    def name(self): return "action_contact_admin"
    
    def run(self, dispatcher, tracker, domain):
        user_msg = tracker.latest_message.get("text", "")
        english = "📞 Support: +92-300-1234567 | support@yourapp.com"
        urdu = "📞 سپورٹ: +92-300-1234567 | ای میل: support@yourapp.com"
        
        if any(u'\u0600' <= c <= u'\u06FF' for c in user_msg):
            dispatcher.utter_message(text=urdu)
        else:
            dispatcher.utter_message(text=translate_response(user_msg, english))
        return []

class ActionLLMFallback(Action):
    def name(self): return "action_llm_fallback"
    
    def run(self, dispatcher, tracker, domain):
        user_msg = tracker.latest_message.get("text", "")
        prompt = f"""User said: "{user_msg}"
        User may be in English or Urdu/Roman Urdu.
        Reply in the SAME language.
        Be helpful - understand bus schedules, parcel tracking, pricing."""
        
        try:
            response = model.generate_content(prompt)
            dispatcher.utter_message(text=response.text.strip())
        except:
            dispatcher.utter_message(text="Sorry, try again! / معاف کیجیے، دوبارہ کوشش کریں!")
        return []
