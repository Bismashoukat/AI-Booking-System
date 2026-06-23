import os
import json
from services.models import Service
from bookings.models import Booking
from .models import ChatSession, BusinessKnowledge
import datetime


ALL_SLOTS = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00']
SLOT_LABELS = {
    '10:00': '10:00 AM', '11:00': '11:00 AM', '12:00': '12:00 PM',
    '13:00': '01:00 PM', '14:00': '02:00 PM', '15:00': '03:00 PM',
    '16:00': '04:00 PM', '17:00': '05:00 PM', '18:00': '06:00 PM',
}


def get_available_slots(date_str):
    try:
        booked = Booking.objects.filter(
            date=date_str,
            status__in=['Pending', 'Confirmed']
        ).values_list('time', flat=True)
        booked_times = [str(t)[:5] for t in booked]
        available = [s for s in ALL_SLOTS if s not in booked_times]
        return available
    except Exception:
        return ALL_SLOTS


def get_services_text():
    services = Service.objects.filter(is_active=True)
    if not services:
        return "We offer various beauty and wellness services."
    lines = []
    for s in services:
        lines.append(f"• {s.name} — {s.duration} mins — Rs. {s.price}")
    return "\n".join(lines)


def find_service(text):
    services = Service.objects.filter(is_active=True)
    text_lower = text.lower()
    for service in services:
        if service.name.lower() in text_lower:
            return service
    for service in services:
        words = service.name.lower().split()
        if any(w in text_lower for w in words if len(w) > 3):
            return service
    return None


def parse_date(text):
    text = text.strip()
    today = datetime.date.today()
    if 'today' in text.lower():
        return str(today)
    if 'tomorrow' in text.lower():
        return str(today + datetime.timedelta(days=1))
    formats = ['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%d %B %Y', '%d %b %Y']
    for fmt in formats:
        try:
            d = datetime.datetime.strptime(text, fmt).date()
            if d >= today:
                return str(d)
        except ValueError:
            continue
    return None


def process_message(session, user_message):
    msg = user_message.strip()
    msg_lower = msg.lower()

    # RESTART
    if any(w in msg_lower for w in ['restart', 'reset', 'start over', 'menu']):
        session.reset()
        return (
            "🔄 Restarted! Hi there! 👋\n\n"
            "I'm your AI receptionist. I can help you:\n"
            "📅 Book an appointment\n"
            "💼 Show our services\n"
            "ℹ️ Answer your questions\n\n"
            "What would you like to do?"
        )

    # GREETING
    if session.step == 'greeting':
        session.step = 'ask_name'
        session.save()
        return (
            "👋 Hello! Welcome!\n\n"
            "I'm your AI receptionist 🤖\n"
            "I can help you book appointments, show services, and answer questions.\n\n"
            "May I have your name please? 😊"
        )

    # GET NAME
    if session.step == 'ask_name':
        if any(w in msg_lower for w in ['book', 'appointment', 'service', 'hello', 'hi']):
            return "Please tell me your name first 😊 (e.g. Bisma)"
        session.user_name = msg.title()
        session.step = 'main_menu'
        session.save()
        return (
            f"Nice to meet you, {session.user_name}! 😊\n\n"
            "How can I help you today?\n\n"
            "Type:\n"
            "📅 **book** — to book an appointment\n"
            "💼 **services** — to see our services & prices\n"
            "❓ **help** — for other questions"
        )

    # MAIN MENU
    if session.step == 'main_menu':

        if any(w in msg_lower for w in ['service', 'services', 'price', 'offer', 'what do you', 'list']):
            services_text = get_services_text()
            return (
                f"💼 Here are our services:\n\n{services_text}\n\n"
                f"Would you like to book one? Just type **book** 😊"
            )

        if any(w in msg_lower for w in ['book', 'appointment', 'schedule', 'reserve', 'want']):
            services = Service.objects.filter(is_active=True)
            if not services:
                return "Sorry, no services available right now."
            session.step = 'select_service'
            session.save()
            service_list = "\n".join([f"{i+1}. {s.name} — Rs. {s.price}" for i, s in enumerate(services)])
            return (
                f"Great {session.user_name}! Let's book your appointment 🎉\n\n"
                f"Which service would you like?\n\n{service_list}\n\n"
                "Type the service name:"
            )

        if any(w in msg_lower for w in ['help', 'info', 'contact', 'hours', 'timing', 'location']):
            knowledge = BusinessKnowledge.objects.all()
            if knowledge:
                answer = "\n\n".join([f"**{k.title}**\n{k.content}" for k in knowledge])
                return f"ℹ️ Here's some info:\n\n{answer}"
            return (
                "ℹ️ We're open Monday to Saturday, 10 AM – 7 PM.\n"
                "📞 Contact: +92-300-0000000\n\n"
                "Type **book** to make an appointment or **services** to see what we offer."
            )

        return (
            f"Hi {session.user_name}! How can I help you?\n\n"
            "📅 **book** — to book an appointment\n"
            "💼 **services** — to see our services\n"
            "❓ **help** — for other questions"
        )

    # SELECT SERVICE
    if session.step == 'select_service':
        service = find_service(msg)
        if not service:
            services = Service.objects.filter(is_active=True)
            service_list = ", ".join([s.name for s in services])
            return f"I couldn't find that service. Please choose from:\n{service_list}"
        session.service = service
        session.step = 'select_date'
        session.save()
        return (
            f"✅ Great choice! **{service.name}** selected.\n"
            f"Duration: {service.duration} minutes | Price: Rs. {service.price}\n\n"
            "📅 What date would you like?\n"
            "Type like: **2026-06-25** or **tomorrow**"
        )

    # SELECT DATE
    if session.step == 'select_date':
        date_str = parse_date(msg)
        if not date_str:
            return (
                "I couldn't understand that date. 😅\n"
                "Please use format like **2026-06-25** or type **tomorrow**"
            )
        available = get_available_slots(date_str)
        if not available:
            return f"Sorry, no slots available on {date_str}. 😔\nPlease try another date:"
        session.selected_date = date_str
        session.step = 'select_time'
        session.save()
        slot_list = "\n".join([f"• {SLOT_LABELS.get(s, s)}" for s in available])
        return (
            f"📅 Date set: **{date_str}**\n\n"
            f"⏰ Available times:\n{slot_list}\n\n"
            "Which time do you prefer? (Type like **14:00** or **02:00 PM**)"
        )

    # SELECT TIME
    if session.step == 'select_time':
        time_input = msg.replace(' ', '').upper()
        matched_slot = None
        for slot in ALL_SLOTS:
            label = SLOT_LABELS.get(slot, slot).replace(' ', '').upper()
            if slot in msg or label in time_input or slot.replace(':', '') in msg:
                matched_slot = slot
                break
        if not matched_slot:
            import re
            m = re.search(r'(\d{1,2}):?(\d{0,2})\s*(AM|PM|am|pm)?', msg)
            if m:
                hour = int(m.group(1))
                ampm = (m.group(3) or '').upper()
                if ampm == 'PM' and hour != 12:
                    hour += 12
                if ampm == 'AM' and hour == 12:
                    hour = 0
                slot_try = f"{hour:02d}:00"
                if slot_try in ALL_SLOTS:
                    matched_slot = slot_try
        if not matched_slot:
            available = get_available_slots(str(session.selected_date))
            slot_list = ", ".join([SLOT_LABELS.get(s, s) for s in available])
            return f"Couldn't match that time. Available: {slot_list}"
        already_booked = Booking.objects.filter(
            date=session.selected_date,
            time=matched_slot + ':00',
            status__in=['Pending', 'Confirmed']
        ).exists()
        if already_booked:
            available = get_available_slots(str(session.selected_date))
            slot_list = "\n".join([f"• {SLOT_LABELS.get(s, s)}" for s in available])
            return (
                f"⚠️ Sorry, {SLOT_LABELS.get(matched_slot, matched_slot)} is already booked!\n\n"
                f"Still available:\n{slot_list}"
            )
        session.selected_time = matched_slot
        session.step = 'confirm'
        session.save()
        return (
            f"⏰ Time set: **{SLOT_LABELS.get(matched_slot, matched_slot)}**\n\n"
            f"📋 Booking Summary:\n"
            f"👤 Name: {session.user_name}\n"
            f"💼 Service: {session.service.name}\n"
            f"📅 Date: {session.selected_date}\n"
            f"⏰ Time: {SLOT_LABELS.get(matched_slot, matched_slot)}\n"
            f"💰 Price: Rs. {session.service.price}\n\n"
            "Shall I confirm this booking? Type **yes** to confirm or **no** to change."
        )

    # CONFIRM
    if session.step == 'confirm':
        if any(w in msg_lower for w in ['yes', 'confirm', 'ok', 'sure', 'haan', 'ji', 'y']):
            try:
                booking = Booking.objects.create(
                    customer_name=session.user_name,
                    phone=session.phone or 'Via Chat',
                    service=session.service,
                    date=session.selected_date,
                    time=session.selected_time + ':00',
                    status='Pending',
                    notes='Booked via AI chatbot'
                )
                session.step = 'done'
                session.save()
                return (
                    f"🎉 **Appointment Confirmed!**\n\n"
                    f"✅ Booking ID: #{booking.id}\n"
                    f"👤 {booking.customer_name}\n"
                    f"💼 {booking.service.name}\n"
                    f"📅 {booking.date}\n"
                    f"⏰ {SLOT_LABELS.get(session.selected_time, session.selected_time)}\n\n"
                    f"We'll see you then! 😊\n"
                    f"Type **book** to make another appointment."
                )
            except Exception as e:
                session.step = 'select_time'
                session.save()
                return f"⚠️ Booking failed: {str(e)}\nPlease try a different time."
        elif any(w in msg_lower for w in ['no', 'nahi', 'nope', 'change', 'n']):
            session.step = 'select_service'
            session.selected_date = None
            session.selected_time = ''
            session.save()
            return "No problem! Let's start again. Which service would you like?"

    # DONE
    if session.step == 'done':
        if any(w in msg_lower for w in ['thank', 'thanks', 'shukriya', 'great', 'nice', 'good']):
            return f"You're welcome {session.user_name}! 😊 See you soon! Type **book** for another appointment."
        if any(w in msg_lower for w in ['book', 'another', 'again']):
            session.step = 'select_service'
            session.selected_date = None
            session.selected_time = ''
            session.service = None
            session.save()
            services = Service.objects.filter(is_active=True)
            service_list = "\n".join([f"{i+1}. {s.name} — Rs. {s.price}" for i, s in enumerate(services)])
            return f"Sure {session.user_name}! Which service?\n\n{service_list}"

    # FALLBACK
    return (
        "I'm not sure I understood that. 😊\n\n"
        "You can type:\n"
        "📅 **book** — to book appointment\n"
        "💼 **services** — to see services\n"
        "🔄 **restart** — to start over"
    )