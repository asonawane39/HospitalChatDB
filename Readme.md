
---

# 🏥 ChatDB: Natural Language Interface for Hospital Data Management

**ChatDB** is a no-code platform that empowers hospital administration staff to efficiently access and manage medical records through **natural language queries**, eliminating the need for technical SQL or NoSQL knowledge.

This system integrates **LLM capabilities** with both **relational** (MySQL) and **NoSQL** (MongoDB) databases to streamline operations like managing prescriptions, appointments, and doctor-patient schedules.

---

## 🚀 Key Features

* 💬 **Natural Language Interface**: Interact with data using plain English instead of SQL/Mongo queries.
* 🏥 **Patient & Doctor Management**: View, update, or delete patient records, prescriptions, and doctor schedules.
* 📅 **Appointment Tracking**: Check available doctors and current appointments.
* ⚡ **LLM-Powered**: Uses Gemini 2.0 Flash for language-to-query conversion.
* 🖥️ **No-Code Experience**: Intuitive interface to save time and reduce manual clicks/filters.

---

## 🛠️ System Requirements

* ✅ **MySQL** – Relational database for structured data
* ✅ **MongoDB** – NoSQL database for unstructured records
* ✅ **Python** – Backend scripting and API handling
* ✅ **ReactJS & npm** – Frontend development

---

## 📦 LLM Integration

* **Model Used**: **Gemini 2.0 Flash**
* **API Key** required for query generation

---

## 🔧 Environment Setup

Before running the project, create a `.env` file in both frontend and backend folders with the following variables:

```env
DB_USERNAME=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_HOST=your_mysql_host
DB_NAME=HOSPITAL
GEMINI_API_KEY=your_gemini_flash_api_key
```

> 💡 **Note:** Backend and frontend are in separate folders and must be run independently.

---

## 🖥️ Running the Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

1. On startup, you’ll be prompted to load initial data:

   * Enter **Y** to load sample data if your database is empty.
   * Enter **N** to proceed if your database is already populated.
2. Choose how to run the app:

   * Type `1` for **server mode** (for frontend integration)
   * Type `2` for **console mode** (CLI interaction)

> 🔗 Server runs at: `http://127.0.0.1:8000`

---

## 🌐 Running the Frontend

```bash
cd frontend
cd UI
npm install
npm run dev
```

> 🌍 Frontend runs at: `http://localhost:5173`

---

## 📚 Summary

| Component | Tech Stack         |
| --------- | ------------------ |
| LLM       | Gemini 2.0 Flash   |
| Backend   | Python (FastAPI)   |
| Frontend  | JavaScript (React) |
| Databases | MySQL, MongoDB     |

---
