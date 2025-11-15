# 🐄 SmartDairy - AI Powered Digital Dairy Management System

A comprehensive digital dairy management system built with Python and Streamlit that helps dairy businesses manage customers, track daily milk entries, generate monthly invoices, and predict future milk quantities using AI forecasting.

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Project Structure](#project-structure)
- [Usage Guide](#usage-guide)
- [Screenshots](#screenshots)
- [Future Scope](#future-scope)

## 🎯 About

SmartDairy is a full-featured dairy management system designed to streamline operations for dairy businesses. It provides an intuitive web interface for managing customers, recording daily milk collections, generating professional invoices, and leveraging AI-powered forecasting to predict future milk quantities.

## ✨ Features

### 1. Customer Management
- ➕ Add new customers with custom pricing
- 📋 View all customers in a organized table
- ✏️ Update customer details (name, price per litre)
- 🗑️ Delete customers (with safety checks)

### 2. Daily Milk Entry
- 📝 Record daily milk quantities for each customer
- 📅 Date-based entry system
- 🔍 Filter entries by date range
- 📥 Export entries to CSV format
- 📊 View all entries in a comprehensive table

### 3. Monthly Billing Module
- 💰 Automatic calculation of monthly bills
- 📊 Summary statistics (total customers, litres, revenue)
- 📄 **PDF Invoice Generation** - Professional, clean invoices
- 📊 **Excel Export** - Formatted spreadsheets with styling
- 📋 **CSV Export** - Simple data export
- 🎨 Beautiful, branded invoice templates

### 4. AI Forecasting
- 🤖 **Moving Average Prediction** - Predict next day's milk quantity
- 📈 Interactive visualization with matplotlib
- 📊 Historical data analysis
- ⚙️ Configurable window size (3-30 days)
- 📉 Trend visualization with predicted values

### 5. Dashboard
- 📊 Real-time statistics
- 📈 Key metrics at a glance
- 📋 Recent entries overview
- 💡 Quick insights

## 🛠️ Tech Stack

- **Python 3.8+** - Core programming language
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **SQLite** - Lightweight database
- **ReportLab** - PDF invoice generation
- **openpyxl** - Excel file creation
- **python-pptx** - PowerPoint presentation generation
- **Matplotlib** - Data visualization and forecasting graphs

## 🚀 Deployment (Make it Available Online)

Want to share SmartDairy with others? Deploy it for free!

### Quick Deploy to Streamlit Cloud (Recommended)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "SmartDairy app"
   git remote add origin https://github.com/YOUR_USERNAME/smartdairy.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select repository: `smartdairy`
   - Main file: `app.py`
   - Click "Deploy"
   - **Done!** Your app will be live at `https://YOUR-APP.streamlit.app`

📖 **Full deployment guide:** See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd smartdairy

# Or simply navigate to the project directory
cd smartdairy
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages:
- streamlit
- pandas
- matplotlib
- reportlab
- python-pptx
- openpyxl

## 🚀 How to Run

1. **Activate your virtual environment** (if using one)

2. **Run the Streamlit application:**

```bash
streamlit run app.py
```

3. **Access the application:**

The application will automatically open in your default web browser at:
```
http://localhost:8501
```

If it doesn't open automatically, you can manually navigate to the URL shown in the terminal.

## 📁 Project Structure

```
smartdairy/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── smartdairy.db              # SQLite database (auto-created)
│
├── utils/                      # Utility modules
│   ├── db.py                  # Database operations
│   ├── billing.py             # Billing and invoice generation
│   └── forecasting.py         # AI forecasting logic
│
├── templates/                  # HTML templates
│   └── invoice_template.html   # Invoice HTML template
│
└── assets/                     # Static assets
    └── logo.png               # Application logo
```

## 📖 Usage Guide

### Getting Started

1. **Launch the application** using `streamlit run app.py`

2. **Add Customers:**
   - Navigate to "Customer Management"
   - Click "Add Customer" tab
   - Enter customer name and price per litre
   - Click "Add Customer"

3. **Record Daily Entries:**
   - Go to "Daily Milk Entry"
   - Select customer, enter quantity and date
   - Click "Add Entry"
   - View and filter entries as needed

4. **Generate Monthly Bills:**
   - Navigate to "Monthly Billing"
   - Select year and month
   - Click "Calculate Billing"
   - Export as PDF, Excel, or CSV

5. **Use AI Forecasting:**
   - Go to "AI Forecasting"
   - Select a customer
   - Adjust moving average window
   - Click "Predict Next Day Quantity"
   - View forecast graph and statistics

### Database

The application automatically creates `smartdairy.db` SQLite database on first run. The database includes:

- **customers** table: Stores customer information
- **entries** table: Stores daily milk entries

No manual database setup required!

## 📸 Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)
*Real-time statistics and recent entries overview*

### Customer Management
![Customer Management](screenshots/customers.png)
*Add, view, update, and delete customers*

### Daily Milk Entry
![Daily Entry](screenshots/entries.png)
*Record and filter daily milk collections*

### Monthly Billing
![Billing](screenshots/billing.png)
*Generate professional invoices in multiple formats*

### AI Forecasting
![Forecasting](screenshots/forecasting.png)
*Predict future milk quantities with visualizations*

## 🔮 Future Scope

### Planned Enhancements

1. **Advanced AI Models**
   - LSTM neural networks for better predictions
   - Seasonal trend analysis
   - Multi-variable forecasting

2. **Enhanced Reporting**
   - Annual reports
   - Customer-wise analytics
   - Profit/loss statements
   - Growth charts

3. **User Management**
   - Multi-user support
   - Role-based access control
   - Authentication system

4. **Mobile App**
   - React Native mobile application
   - Offline mode support
   - Push notifications

5. **Integration Features**
   - SMS/Email invoice delivery
   - Payment tracking
   - Integration with accounting software
   - Barcode scanning for quick entry

6. **Advanced Analytics**
   - Customer behavior analysis
   - Price optimization suggestions
   - Inventory management
   - Supply chain optimization

7. **Cloud Deployment**
   - Cloud database support
   - Multi-location support
   - Real-time synchronization

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Developed as a final-year project demonstrating full-stack development skills with Python and Streamlit.

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- All open-source libraries used in this project
- The dairy management community for inspiration

---

**🐄 SmartDairy - Making Dairy Management Smarter!**

For support or questions, please open an issue in the repository.

