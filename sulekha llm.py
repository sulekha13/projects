# -*- coding: utf-8 -*-
"""sulekha.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13vsKbXmyP1dWTsb44RTuK5Mq4ICc75Fs
"""

from google.colab import drive
drive.mount('/content/drive')

from google.colab import files
uploaded=files.upload()
print(uploaded)

import pandas as pd

df = pd.read_csv("hotel_bookings.csv")
df.dropna(inplace=True)  # Remove missing values
df["reservation_status_date"] = pd.to_datetime(df["reservation_status_date"])
print(df)

df['revenue'] = df['adr'] * df['stays_in_week_nights']  # Example revenue calculation
revenue_trend = df.groupby('reservation_status_date')['revenue'].sum()
revenue_trend.plot()

cancellation_rate = df[df['is_canceled'] == 1].shape[0] / df.shape[0] * 100
print(cancellation_rate)

import seaborn as sns
sns.countplot(y=df['country'])

import matplotlib.pyplot as plt
plt.hist(df['lead_time'], bins=50)

!pip install faiss-cpu
from sentence_transformers import SentenceTransformer
import faiss # This line was causing the error before installing the faiss-cpu package
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
vector_data = model.encode(df['hotel'].astype(str).tolist())
index = faiss.IndexFlatL2(vector_data.shape[1])
index.add(np.array(vector_data))
print(index)

!pip install fastapi uvicorn nest-asyncio pyngrok

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import sqlite3
import nest_asyncio
from pyngrok import ngrok
import uvicorn

# Allow nested event loops in Colab
nest_asyncio.apply()

# Load data (if you're using a CSV)
df = pd.read_csv("hotel_bookings.csv")

# Save to SQLite for demo
conn = sqlite3.connect("hotel_data.db")
df.to_sql("hotel_bookings", conn, if_exists="replace", index=False)

# FastAPI app
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hotel Booking API is live!"}

@app.get("/bookings")
def get_bookings(limit: int = 5):
    conn = sqlite3.connect("hotel_data.db")
    data = pd.read_sql(f"SELECT * FROM hotel_bookings LIMIT {limit}", conn)
    return data.to_dict(orient="records")

!curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
	| sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
	&& echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
	| sudo tee /etc/apt/sources.list.d/ngrok.list \
	&& sudo apt update \
	&& sudo apt install ngrok
!curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
	| sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
	&& echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
	| sudo tee /etc/apt/sources.list.d/ngrok.list \
	&& sudo apt update \
	&& sudo apt install ngrok

!ngrok config add-authtoken 2ufdhai9FT0UAt6C6YdRF7pO3xi_JFDXQDJH1igzNooSVHhW

!apt-get install -y grok
!grok http http://localhost:8080

# Launch API using ngrok
public_url = ngrok.connect(8000)
print(f"🌍 Public API: {public_url}")

uvicorn.run(app, port=8000)

@app.get("/analytics/cancellation_rate")
def get_cancellation_rate():
    conn = sqlite3.connect("hotel_data.db")
    q = """
    SELECT
        ROUND(SUM(CASE WHEN is_canceled = 1 THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) AS cancellation_rate
    FROM hotel_bookings
    """
    result = pd.read_sql(q, conn)
    return result.to_dict(orient="records")[0]

import timeit
import requests

def test_api_response_time():
    # Measure the time taken to call the API
    response_time = timeit.timeit(
        stmt="requests.post('http://127.0.0.1:8000/analytics')",
        setup="import requests",
        number=10  # Number of API calls
    )
    print(f"Average response time over 10 calls: {response_time / 10:.4f} seconds")

test_api_response_time()

import sqlite3

# Connect to (or create) a SQLite database
conn = sqlite3.connect("hotel_data.db")

# Save the DataFrame to a SQL table called 'hotel_bookings'
df.to_sql("hotel_bookings", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

# Reconnect to check the data
conn = sqlite3.connect("hotel_data.db")

# Run a sample query
result_df = pd.read_sql("SELECT * FROM hotel_bookings LIMIT 5", conn)
conn.close()

# Show result
result_df

from google.colab import files
files.download("hotel_data.db")

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sqlite3
import pandas as pd
import sys
import importlib
from datetime import datetime

app = FastAPI()

@app.get("/health")
def health_check():
    status = {
        "status": "ok",
        "database": "connected",
        "dependencies": {},
        "timestamp": datetime.now().isoformat()
    }

    # ✅ Check SQLite database connection
    try:
        conn = sqlite3.connect("hotel_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
    except Exception as e:
        status["status"] = "error"
        status["database"] = f"disconnected: {str(e)}"

    # ✅ Check installed dependencies
    try:
        status["dependencies"] = {
            "python": sys.version,
            "pandas": pd.__version__,
            "fastapi": importlib.import_module("fastapi").__version__,
            "sqlite3": sqlite3.version
        }
    except Exception as e:
        status["status"] = "error"
        status["dependencies_error"] = str(e)

    # ⛔ Return 500 if there are any errors
    if status["status"] != "ok":
        return JSONResponse(status_code=500, content=status)

    return status

{
  "status": "ok",
  "database": "connected",    #Response When Everything is Healthy
  "dependencies": {
    "python": "3.10.12 (default, Nov 23 2023, 12:00:00) [GCC 11.3.0]",
    "pandas": "2.1.4",
    "fastapi": "0.110.0",
    "sqlite3": "2.6.0"
  },
  "timestamp": "2025-03-22T21:13:05.781235"
}
