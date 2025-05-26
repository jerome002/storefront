
# 🛒 Storefront App

A lightweight web-based sales and expense tracker built with Flask and Supabase, developed as part of the **Vibe Coding Hackathon**.

---

## ✨ Features

- ✅ Track sales and expenses
- 🧾 Upload receipt photos
- 🕒 View transaction history
- 📊 Visualize data with charts *(optional)*
- 📁 Export data to CSV/PDF *(optional)*
- 🎙️ Voice input for quick logging *(optional)*

---

## 🛠 Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, Bootstrap 5, Jinja2
- **Database:** Supabase (PostgreSQL)
- **Hosting:** Render *(or Vercel for frontend frameworks)*

---

## 📂 Project Structure

```
storefront/
│
├── app.py                  # Main Flask app
├── templates/              # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── add_sale.html
│   └── add_expense.html
├── static/                 # CSS, JS, images
│
├── supabase/               # Supabase config or helper scripts
├── requirements.txt        # Python dependencies
└── README.md               # You're here!
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/jerome002/storefront.git
cd storefront
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add your Supabase credentials:

```env
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-api-key
```

### 5. Run the App

```bash
flask run
```

---

## 📸 Screenshots

_Add screenshots of the dashboard, receipt upload, or data tables here._

---

## 🚀 Future Enhancements

- 📈 Add Chart.js visualizations for interactive data insights
- 🧾 Export to CSV and PDF formats
- 🎙️ Integrate voice-to-text for faster input and accessibility
- 🔐 Add user authentication (Supabase Auth or Flask-Login)
- 📱 Enhance mobile responsiveness and offline support
- ✅ Set up automated testing and CI/CD pipelines
- 👥 Support multi-user and team-based features
- 🏷️ Add customizable categories and tags for transactions
- 📊 Improve dashboard analytics and reporting
- 🔔 Integrate notifications and reminders

---

## 👨‍💻 Author

**Jerome Kapkor Kimosop**  
📧 [jkapkor@gmail.com](mailto:jkapkor@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/jeromekapkor) | [GitHub](https://github.com/jerome002)
