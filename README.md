KrishiMitra - A Modern Farm Management System
📖 About the Project
KrishiMitra is a web-based farm management dashboard designed to help farmers modernize their operations. It replaces traditional paper-based record-keeping with a clean, digital interface, allowing for efficient tracking of crops, inventory, livestock, and finances. The application features separate, secure dashboards for both farmers and administrators, providing tools for data-driven decision-making and platform oversight.
This project was developed as a mini-project for the Bachelor of Engineering in Information Technology curriculum.

✨ Key Features
For Farmers (User Dashboard)
Secure Authentication: Secure user registration with password validation and login.
Interactive Dashboard: An at-a-glance overview of key farm metrics with clickable cards for quick navigation.
Resource Management: Full CRUD (Create, Read, Update, Delete) functionality for:
  🌱 Crops: Track sowing dates, harvest dates, area, and financials.
  📦 Inventory: Manage stock levels for items like seeds and fertilizers.
  🐄 Livestock: Keep records of animal types, counts, and health statuses.
  👨‍🌾 Workers: Manage employee information.
Financial Analytics: A line chart visualizes monthly profit to track financial performance.

Smart Widgets:
Planting Guide: A static guide for seasonal crops in the Maharashtra region.
Alerts & Reminders: Proactive notifications for low inventory, sick livestock, and upcoming harvests.

For Administrators (Admin Dashboard)
Platform Analytics: A comprehensive overview of the entire platform with charts for:
Most common crops and livestock distribution.
Top-performing users by revenue.
Platform-wide inventory levels.
Monthly harvest vs. wastage trends.
User Management: A simple interface to view a list of all registered users and the ability to delete accounts.
Broadcast System: A tool to send announcements to all registered users.

🛠️ Technology Stack
Frontend: HTML5, Tailwind CSS, JavaScript
Charting Library: Chart.js
Backend: Python
Web Framework: Flask
Database: PostgreSQL
Password Security: bcrypt for hashing

🚀 Getting Started
Follow these instructions to get a local copy of the project up and running.

Prerequisites
Python 3.x installed on your system.
pip (Python package installer).

A running instance of PostgreSQL.

Installation & Setup
Clone the Repository
git clone [https://github.com/YourUsername/KrishiMitra.git](https://github.com/YourUsername/KrishiMitra.git)
cd KrishiMitra

Set up the Backend
Navigate to the backend directory:
cd backend

Create and activate a virtual environment:
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install the required Python packages:
pip install -r requirements.txt

Configure your database connection in db.py.

Run the Flask application:
flask run
Your backend API will now be running at http://127.0.0.1:5000.

Run the Frontend
The frontend is built with simple HTML files. You can open them directly in your browser.
For the best experience, use a live server extension in your code editor (like "Live Server" in VS Code).
Open the frontend folder and launch the index.html or login.html file.

usage
Navigate to the registration.html page to create a new user account.
Log in using the login.html page.
Once logged in, you will be directed to your personal dashboard where you can start managing your farm data.
To access the admin panel, log in with an account that has the isAdmin flag set to true in the database.

📁 Project Structure
├── .gitignore
├── README.md
├── backend
    ├── app.py
    ├── db.py
    ├── middleware
    │   └── auth_middleware.py
    ├── requirements.txt
    └── routes
    │   ├── admin.py
    │   ├── auth.py
    │   ├── broadcasts.py
    │   ├── crops.py
    │   ├── inventory.py
    │   ├── livestock.py
    │   └── workers.py
└── frontend
    ├── admin-dashboard.html
    ├── assets
        └── farm-background.jpg
    ├── index.html
    ├── login.html
    ├── registration.html
    └── user-dashboard.html
