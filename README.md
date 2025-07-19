# 📊 BRVM Stock Data Scraper

This project is a fully automated **web scraper** for extracting stock market data from the [BRVM (Bourse Régionale des Valeurs Mobilières)](https://www.brvm.org/) website. It runs daily (Monday to Friday) via GitHub Actions, cleans and transforms the data, and stores it in a PostgreSQL database.

---

## 🚀 Features

- Scrapes **stock action data** (symbol, price, volume, etc.)
- Auto-converts and cleans data (e.g., % changes, price formatting)
- Pushes to a **remote PostgreSQL** database
- Uses **GitHub Actions** to run every weekday at 08:00 UTC
- Credentials managed securely via **GitHub Secrets**

---

## 🐍 Tech Stack

- Python 3.10+
- Selenium (headless browser automation)
- Pandas (data processing)
- SQLAlchemy (PostgreSQL connection)
- GitHub Actions (CI automation)
- dotenv (local environment variable support)

---

## 📁 Project Structure

```bash
brvm-stockdata-scraper/
├── brvm-scraper/                 # Main source folder
│   └── scraper.py                # Web scraping and DB insertion script
├── .github/
│   └── workflows/
│       └── scraper.yml           # GitHub Actions CI workflow
├── .env.example                  # Environment variable template
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation (this file)
```

---

## ⚙️ Environment Variables

These environment variables must be added as **GitHub Secrets** in your repository:

| Secret Name    | Description                    |
|----------------|--------------------------------|
| `DB_USER`       | PostgreSQL username            |
| `DB_PASSWORD`   | PostgreSQL password            |
| `DB_HOST`       | PostgreSQL host (e.g. RDS URL) |
| `DB_PORT`       | PostgreSQL port (usually 5432) |
| `DB_NAME`       | PostgreSQL database name       |

Create a `.env` file locally for testing based on this template:

```env
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_host
DB_PORT=5432
DB_NAME=brvmdatabase
## 🔄 GitHub Actions Automation

The scraper is fully automated and runs **Monday–Friday at 08:00 UTC** using GitHub Actions.
````
### ✅ Status: **Enabled and Working**

The GitHub Actions workflow has been configured and is already running as scheduled.

---

### 📌 Trigger the Workflow Manually (Already Set Up)

To run the scraper manually:

1. Go to your GitHub repository: [brvm-stockdata-scraper](https://github.com/idrissbado/brvm-stockdata-scraper)
2. Click on the **Actions** tab.
3. Select the workflow: **BRVM Stock Data Scraper**
4. Click **Run workflow** (top right)
5. Confirm to run the workflow on `main`

This will start the data extraction and push to the database.

