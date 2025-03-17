🧾 Billing & Inventory Management System
📌 Overview
The Billing & Inventory Management System is a lightweight, efficient, and user-friendly web application built to streamline sales, purchase, and stock management processes. Designed for both retail and wholesale businesses, it offers core features like GST/Non-GST invoicing, real-time stock updates, customer and seller management, payment tracking, and image-based bill entry.

This project leverages a simple and maintainable tech stack:
HTML/CSS/JavaScript for frontend, Flask (Python) for backend APIs, and MySQL for the database.

🚀 Key Features
GST/Non-GST Sales & Purchase Billing
Real-Time Stock Updates with Alerts
Product Search by Code, Type, Subtype & Specifications
Single-Page Order Entry Form with Auto-Suggestions
Customer, Seller, and Area Management
Estimate Generation with WhatsApp/Email Sharing
Payment Tracking & Outstanding Dues Management
Purchase Order Creation & Stock Refill Notifications
Image-Based Bill Entry with Data Extraction to JSON
Soft Delete Implementation (IS_ACTIVE / DELETED_FLAG flags)
🛠️ Tech Stack
Component	Technology
Frontend	HTML, CSS, JavaScript
Backend	Flask (Python)
Database	MySQL
Optional Tools	Bootstrap (for UI), REST APIs
📂 Project Structure
bash
Copy
Edit
/billing-system/
├── /static/                # CSS, JS, images
├── /templates/             # HTML files (Jinja templates)
├── /app/                   # Flask application package
│   ├── __init__.py         # App factory
│   ├── routes.py           # Route handlers (views)
│   ├── models.py           # SQLAlchemy models
│   └── utils.py            # Helper functions (image processing, etc.)
├── /migrations/            # Database migrations
├── /scripts/               # SQL setup scripts
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
🏗️ Installation & Setup Instructions
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/yourusername/billing-system.git
cd billing-system
2. Set up Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
3. Install Python Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Configure Database
Create a MySQL database:
sql
Copy
Edit
CREATE DATABASE billing_db;
Update database credentials in config.py:
python
Copy
Edit
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/billing_db'
5. Initialize Database
bash
Copy
Edit
flask db init
flask db migrate
flask db upgrade
6. Run Flask Server
bash
Copy
Edit
flask run
The server will be available at: http://localhost:5000

💡 Usage
Login: Admin or Salesman access.
Add/Edit Products, Categories, Sellers, Customers.
Create Purchase Orders & Update Stock.
Generate Sales Bills using product search with auto-suggestions.
Send Estimates through WhatsApp or Email.
Track Payments & Pending Dues.
Monitor stock alerts and create Purchase Orders.
Upload scanned bills, system auto-converts them to JSON for entry.
View reports: Sales, Purchases, Payments, Stock, etc.
🗃️ Core Database Tables
STOCK_DETAILS
SELLERS_DTL
CUSTOMER_LIST
PURCHASE_ORDER
PURCHASE_AUDIT
SELL_ORDER
SELL_AUDIT
PRODUCT_BILL_TRACKER
AREA_LIST
📸 Additional Features
Image-Based Bill Entry: Upload scanned or image files, auto-extract bill data to JSON.
Soft Deletes: Safe archival of records using IS_ACTIVE or DELETED_FLAG.
Simple & Responsive UI: Clean, fast-loading interface optimized for desktops.
✨ Future Scope
Add payment gateway integration (UPI, cards).
Role-based user permissions.
Enhanced dashboards & reporting.
Mobile app extension using the same backend API.
📬 Contact
For questions, feature requests, or collaboration:

Email:raiamarjeet01@gmail.com
Phone: +91-8709546640

