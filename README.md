
# 🤖 AI Appointment Booking System

> An AI-powered receptionist system that handles customer chats, bookings, and business management automatically.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![AI](https://img.shields.io/badge/AI-Powered-purple)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)

---

## 🚀 Live Demo
> Coming soon on Render.com

---

## 📌 What is this?

This is a **SaaS-style AI receptionist system** built for small businesses like skin clinics, beauty salons, and dental clinics.

Instead of hiring a receptionist, businesses can use this system to:
- Handle customer queries 24/7 via AI chat
- Accept appointments automatically
- Manage bookings from a dashboard
- Send confirmations and reminders

---

## ✨ Features

### 🤖 AI Chatbot
- Natural conversation flow
- Step-by-step booking via chat
- Service information & FAQs
- Business knowledge base

### 📅 Smart Booking Engine
- Real-time slot availability
- Double booking protection
- Auto confirmation
- Reschedule & cancel support

### 🏢 Owner Dashboard
- Today's appointments view
- All bookings with filters
- Status management (Confirm/Cancel/Complete)
- Business stats & overview

### 👥 CRM System
- Customer details saved automatically
- Visit history tracking
- Booking status tracking
- Notes system

### 🧠 Knowledge Base
- Owner adds business info
- AI uses it to answer customer questions
- Working hours, location, policies, prices

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django (Python) |
| Database | SQLite → PostgreSQL (production) |
| Frontend | Django Templates + Vanilla JS |
| AI Layer | Rule-based Engine (Groq AI ready) |
| Deployment | Render.com |

---

## 📁 Project Structure

```
AI_Booking_System/
│
├── core/               # Django settings & URLs
├── services/           # Service management
├── bookings/           # Booking engine
├── chatbot/            # AI chatbot brain
├── dashboard/          # Owner panel
├── accounts/           # Authentication
├── templates/          # HTML templates
└── static/             # CSS & JS
```

---

## ⚙️ Setup & Installation

```bash
# 1. Clone the repo
git clone https://github.com/Bismashoukat/AI_Booking_System.git
cd AI_Booking_System

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser

# 6. Run server
python manage.py runserver
```

---

## 🌐 URLs

| URL | Description |
|-----|-------------|
| `/chatbot/` | AI Chat Interface (for customers) |
| `/bookings/` | Direct Booking Form |
| `/services/` | Services List |
| `/dashboard/` | Owner Dashboard |
| `/admin/` | Django Admin |

---

## 🎯 Target Industries

- 💆 Skin Clinics & Beauty Salons
- 🦷 Dental Clinics
- 🏋️ Fitness & Wellness Centers
- 🏠 Real Estate Agencies
- 📚 Coaching & Training Centers

---

## 💰 Business Value

| Problem | Solution |
|---------|----------|
| Manual receptionist cost | AI handles 24/7 for free |
| Missed appointments | Auto reminders system |
| Double bookings | Smart slot protection |
| After-hours queries | AI chatbot always available |
| Lead capture | Auto CRM saves every customer |

---

## 🔮 Roadmap

- [x] AI Chatbot with booking flow
- [x] Smart slot management
- [x] Owner dashboard
- [x] Knowledge base
- [ ] Groq AI integration (natural language)
- [ ] WhatsApp bot integration
- [ ] Email/SMS reminders
- [ ] Multi-business support (SaaS)
- [ ] Payment integration

---

## 👩‍💻 Built By

**Bisma Shoukat**
- 🌐 [LinkedIn](https://linkedin.com/in/bisma-shoukat-50ab88378)
- 💼 [Fiverr](https://fiverr.com/bismacoder)
- 🐙 [GitHub](https://github.com/Bismashoukat)

> Freelance AI Automation Developer | Django | n8n | Chatbots | CRM Systems

---

## 📄 License

MIT License — Free to use and modify.

## Built by: Bisma Shoukat
