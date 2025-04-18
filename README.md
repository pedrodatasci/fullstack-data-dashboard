# 📊 Fullstack Dashboard with Flask, Dash and PostgreSQL

This project is a complete fullstack data dashboard built with:

- 🐍 Flask for API creation  
- 📈 Dash + Plotly for interactive data visualization  
- 🐘 PostgreSQL for data persistence  
- 🐳 Docker-ready structure for deployment  
- 🧪 Fake data seeding included automatically on first run  

---

## ✨ Features

- REST API to register and list data  
- Interactive dashboard with daily aggregation  
- 7-day dual forecast: Linear Regression and Holt-Winters  
- Automatic seeding of 100+ fake records for demo purposes  
- Modular and production-ready structure  

---

## 📦 Tech Stack

- Python 3.10+  
- Flask  
- Dash / Plotly  
- SQLAlchemy  
- PostgreSQL  
- scikit-learn  
- statsmodels  
- Docker (optional)  
- pandas / requests  

---

## 📁 Project Structure

```
project/
├── app/
│   ├── __init__.py            # App factory + data seeding
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py          # REST API routes
│   ├── db/
│   │   ├── __init__.py
│   │   └── models.py          # SQLAlchemy model
│   └── dashapp/
│       ├── __init__.py
│       └── dashboard.py       # Dash layout and logic with dual forecast
├── run.py                     # Entry point for running the app
├── requirements.txt           # Python dependencies
├── docker-compose.yml         # (Optional) Docker setup
└── README.md
```

---

## ▶️ How to Run Locally

### 1. Clone the project

```bash
git clone https://github.com/pedrodatasci/fullstack-data-dashboard.git
cd fullstack-data-dashboard
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL (Docker or local)

Make sure PostgreSQL is running and accessible at:

```
postgresql://user:password@localhost:5432/insights
```

### 5. Run the application

```bash
python run.py
```

- API: [http://localhost:5000/api/records](http://localhost:5000/api/records)  
- Dashboard: [http://localhost:5000/dashboard/](http://localhost:5000/dashboard/)

---

## 📊 Dashboard Preview

- First chart: daily values + 7-day forecast using **Linear Regression**  
- Second chart: same data projected with **Holt-Winters (Exponential Smoothing)**  
- Third chart: comparison of both forecasts side-by-side (line chart)  
- Fake data seeded automatically if no records exist  

---

## 📌 Notes

- `venv/` should not be committed. Use `.gitignore`.  
- Dashboard supports extensibility (filters, export, themes).  
- Ready for cloud deployment (AWS, GCP, Azure).  

---

## 🧐 Author

Pedro Sá  
[LinkedIn](https://www.linkedin.com/in/pedro-sofiati-de-sa/) · [GitHub](https://github.com/pedrodatasci)

---

## 📜 License

MIT License