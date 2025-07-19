import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from sqlalchemy import text
import numpy as np
from sqlalchemy import bindparam
from dotenv import load_dotenv
import os

# Configure headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL to scrape
url = "https://www.brvm.org/en/cours-actions/0"
driver.get(url)
time.sleep(5)  # Wait for JavaScript to load content

# Find all rows in the table
rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")

# Extract data row by row
data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) >= 7:
        symbol = cols[0].text.strip()
        name = cols[1].text.strip()
        volume = cols[2].text.strip().replace('\xa0', ' ')
        prev_price = cols[3].text.strip().replace('\xa0', ' ')
        open_price = cols[4].text.strip().replace('\xa0', ' ')
        close_price = cols[5].text.strip().replace('\xa0', ' ')
        change_pct = cols[6].text.strip()
        data.append([symbol, name, volume, prev_price, open_price, close_price, change_pct])

# Close browser
driver.quit()

# Convert to DataFrame
df = pd.DataFrame(data, columns=[
    "SYMBOL", "NAME", "VOLUME", "PREVIOUS_PRICE", "OPENING_PRICE", "CLOSING_PRICE", "CHANGE_PERCENT"
])

# Data Cleaning - standardize numbers
for col in ["VOLUME", "PREVIOUS_PRICE", "OPENING_PRICE", "CLOSING_PRICE"]:
    df[col] = df[col].str.replace(' ', '').str.replace(',', '.').astype(float)

# Clean percentage
df["CHANGE_PERCENT"] = df["CHANGE_PERCENT"].str.replace('%', '').str.replace(',', '.').astype(float)

# Add update date
df["UPDATE_DATE"] = pd.Timestamp.today().normalize()

target_postgres_engine = create_engine(f"postgresql://{target_db_params_postgres['user']}:{target_db_params_postgres['password']}@{target_db_params_postgres['host']}:{target_db_params_postgres['port']}/{target_db_params_postgres['database']}")
# Create the new column by combining SYMBOL and UPDATE_DATE without spaces
df['ID'] = df['SYMBOL'] + '-' + df['UPDATE_DATE'].str.replace(' ', '')
df=pd.DataFrame(df)

# First rename DataFrame columns to match database schema
df = df.rename(columns={
    'PREVIOUS_PRICE': 'PREVIOUS_PR',
    'OPENING_PRICE': 'OPENING_PR',
    'CLOSING_PRICE': 'CLOSING_PRI',
    'CHANGE_PERCENT': 'CHANGE_PEF'
})

load_dotenv()
target_db_params_postgres = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}
# Now insert with correct SQLAlchemy syntax
with target_postgres_engine.begin() as connection:
    for _, row in df.iterrows():
        # Create a SQLAlchemy text() object
        stmt = text("""
            INSERT INTO actions (ID, SYMBOL, NAME, VOLUME, PREVIOUS_PR, OPENING_PR, 
                               CLOSING_PRI, CHANGE_PEF, UPDATE_DATE)
            VALUES (:ID, :SYMBOL, :NAME, :VOLUME, :PREVIOUS_PR, 
                   :OPENING_PR, :CLOSING_PRI, :CHANGE_PEF, :UPDATE_DATE)
            ON CONFLICT (ID) DO UPDATE SET
                SYMBOL = EXCLUDED.SYMBOL,
                NAME = EXCLUDED.NAME,
                VOLUME = EXCLUDED.VOLUME,
                PREVIOUS_PR = EXCLUDED.PREVIOUS_PR,
                OPENING_PR = EXCLUDED.OPENING_PR,
                CLOSING_PRI = EXCLUDED.CLOSING_PRI,
                CHANGE_PEF = EXCLUDED.CHANGE_PEF,
                UPDATE_DATE = EXCLUDED.UPDATE_DATE
        """)
        
        # Execute with parameters
        connection.execute(stmt, {
            'ID': row['ID'],
            'SYMBOL': row['SYMBOL'],
            'NAME': row['NAME'],
            'VOLUME': row['VOLUME'],
            'PREVIOUS_PR': row['PREVIOUS_PR'],
            'OPENING_PR': row['OPENING_PR'],
            'CLOSING_PRI': row['CLOSING_PRI'],
            'CHANGE_PEF': row['CHANGE_PEF'],
            'UPDATE_DATE': row['UPDATE_DATE']
        })