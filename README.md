```markdown
# KrishiMitra Pro 🌾

An enterprise-grade agricultural intelligence platform designed to bridge the gap between farm-level operations and global agricultural data. KrishiMitra Pro provides a comprehensive suite for farmers to manage crops, livestock, inventory, and workforce, while offering administrators a powerful command center for platform-wide analytics and real-time market intelligence.

---

## 🚀 Key Features

### 🧑‍🌾 Farmer Node (User Dashboard)
* **Production Cycles:** Initiate and track crop batches from sowing to harvest with stage-specific verifications.
* **Livestock & Workforce Hub:** Manage livestock health, yields, and track worker assignments, tasks, and daily wages.
* **Asset Ledger:** Maintain a real-time inventory of fertilizers, seeds, and equipment with an automated upsert engine.
* **Audit Vault:** Generate professional, two-column PDF balance sheets for every completed harvest cycle.

### 🏢 Command Center (Admin Dashboard)
* **Global Telemetry:** Monitor active nodes, total platform capital flow, and aggregate network asset values.
* **Market IQ Sync:** Fetch and broadcast live Mandi pricing data (Agmarknet integration).
* **Master Directory:** Searchable ledger of all verified farmer identities and their financial footprints.
* **System Control:** Broadcast urgent alerts to all nodes and toggle system-wide maintenance modes.

---

## 🛠️ Tech Stack

**Frontend:**
* HTML5 / CSS3
* [Tailwind CSS](https://tailwindcss.com/) (Rapid UI styling)
* [Chart.js](https://www.chartjs.org/) (Data visualization)
* [jsPDF](https://parall.ax/products/jspdf) (Client-side PDF generation)

**Backend:**
* [Python 3](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/) (RESTful API framework)
* [SQLAlchemy](https://www.sqlalchemy.org/) (ORM for database management)
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) (Data scraping for Market IQ)

---

## 📂 Project Structure

```text
├── .gitignore
├── README.md
├── backend/
│   ├── app.py                     # Main application entry point & blueprint registration
│   ├── db.py                      # SQLAlchemy database models
│   ├── middleware/
│   │   └── auth_middleware.py     # Authentication interceptors & RBAC
│   ├── requirements.txt           # Python backend dependencies
│   └── routes/
│       ├── admin.py               # Global analytics, directory, and system controls
│       ├── auth.py                # User registration, login, and session handling
│       ├── broadcasts.py          # Admin messaging and alert distribution
│       ├── crops.py               # Crop lifecycle and yield tracking
│       ├── inventory.py           # Stock management and resource ledger
│       ├── livestock.py           # Livestock tracking and management
│       └── workers.py             # Labor task assignments and wage logging
└── frontend/
    ├── admin-dashboard.html       # Enterprise command center UI
    ├── index.html                 # Platform landing page
    ├── login.html                 # Authentication gateway
    ├── registration.html          # New node onboarding
    ├── user-dashboard.html        # Farmer operations portal
    └── assets/
        └── farm-background.jpg    # UI background assets
```

---

## 💻 Installation & Setup

Follow these steps to run the application locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/krishimitra-pro.git](https://github.com/yourusername/krishimitra-pro.git)
cd krishimitra-pro
```

### 2. Backend Setup
Navigate to the backend directory and set up your Python environment:
```bash
cd backend

# Create a virtual environment (Recommended)
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (Create a .env file)
echo "DATABASE_URL=sqlite:///krishimitra.db" > .env
echo "SECRET_KEY=your_super_secret_key" >> .env

# Initialize the database and run the server
python app.py
```
*The backend API will start running on `http://127.0.0.1:5000`.*

### 3. Frontend Setup
The frontend is built with vanilla HTML/JS and uses CDN links for frameworks. No build step is required. Open `frontend/index.html` in any modern web browser, or use a local development server like the **Live Server** extension in VS Code.

---

## 🔒 Authentication & Access

* **Farmers:** Register via `registration.html`. Upon successful login, you will be directed to the `user-dashboard.html`.
* **Administrators:** Requires backend database configuration. Run a SQL update command (e.g., `UPDATE users SET is_admin = TRUE WHERE email = 'admin@gmail.com';`) to grant access to the `admin-dashboard.html` features.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
```