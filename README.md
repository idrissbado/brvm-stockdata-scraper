# 📊 BRVM Stock Data Scraper

A Python web scraper that automatically extracts BRVM market data and stores it in a PostgreSQL database using GitHub Actions.

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

## 🔄 GitHub Actions Automation

The scraper is fully automated and runs **Monday–Friday at 10:00 UTC** using GitHub Actions.

### ✅ Status: **Enabled and Working**

The GitHub Actions workflow has been configured and is already running as scheduled.

### 🕹 Trigger the Workflow Manually

1. Go to your GitHub repository: [brvm-stockdata-scraper](https://github.com/idrissbado/brvm-stockdata-scraper)
2. Click on the **Actions** tab.
3. Select the workflow: **BRVM Stock Data Scraper**
4. Click **Run workflow** (top right)
5. Confirm to run the workflow on `main`

---

## 🧪 Run Locally

To test or develop the scraper locally:

```bash
git clone https://github.com/idrissbado/brvm-stockdata-scraper.git
cd brvm-stockdata-scraper

# (optional) create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your DB credentials

# Run the scraper
python brvm-scraper/scraper.py
```

---

## 🚀 Deployment

All deployments are handled by **GitHub Actions**.

After making changes, simply:

```bash
git add .
git commit -m "Update script or workflow"
git push origin main
```

Your scraper will execute automatically based on the schedule or via manual trigger.

---

## 🔐 GitHub Secrets

Make sure the following secrets are set in your GitHub repository under **Settings > Secrets and variables > Actions**:

- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`

These will be used during GitHub Actions execution for secure DB connection.

---

## 📜 License

This project is open-source and available under the **MIT License**.

---

## 🙌 Credits

- [BRVM](https://www.brvm.org) for market data
- [Selenium](https://www.selenium.dev/) for browser automation
- [GitHub Actions](https://github.com/features/actions) for CI/CD
- Built with 💡 by [@idrissbado](https://github.com/idrissbado)

---

## 🧾 GitHub Actions Workflow (for reference)

```yaml
name: BRVM Stock Data Scraper

on:
  schedule:
    - cron: '0 8 * * 1-5'  # 08:00 UTC Monday to Friday
  workflow_dispatch:

jobs:
  scrape_and_store:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run scraper
      env:
        DB_USER: ${{ secrets.DB_USER }}
        DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        DB_HOST: ${{ secrets.DB_HOST }}
        DB_PORT: ${{ secrets.DB_PORT }}
        DB_NAME: ${{ secrets.DB_NAME }}
      run: |
        python brvm-scraper/scraper.py
```
