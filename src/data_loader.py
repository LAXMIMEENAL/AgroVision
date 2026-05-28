
import pandas as pd
import numpy as np
from src.weather_api import get_weather
from src.ndvi_api import get_live_ndvi
def load_data():

    # -----------------------------
    # Load Original Dataset
    # -----------------------------
    df = pd.read_csv("data/dataset.csv")
    df = df.sample(100).reset_index(drop=True)
    # -----------------------------
    # Set Random Seed
    # -----------------------------
    # Ensures same random values every run
    np.random.seed(42)

    # -----------------------------
    # Add NDVI Values
    # -----------------------------
    # NDVI range:
    # 0.2 -> unhealthy vegetation
    # 0.9 -> healthy vegetation

    df["ndvi"] = np.random.uniform(
        0.2,
        0.9,
        len(df)
    )


    # -----------------------------
    # Add Geographic Coordinates
    # -----------------------------
    # Simulated farm locations in India
    
    india_farm_locations = [
    (28.7041, 77.1025),   # Delhi
    (19.0760, 72.8777),   # Mumbai
    (13.0827, 80.2707),   # Chennai
    (22.5726, 88.3639),   # Kolkata
    (17.3850, 78.4867),   # Hyderabad
    (12.9716, 77.5946),   # Bangalore
    (26.9124, 75.7873),   # Jaipur
    (23.0225, 72.5714),   # Ahmedabad
    (11.0168, 76.9558),   # Coimbatore
    (15.3173, 75.7139)    # Karnataka region
    ]

    locations = np.random.choice(
        len(india_farm_locations),
     len(df)
    )

    df["lat"] = [
     india_farm_locations[i][0]
     + np.random.uniform(-0.5, 0.5)
        for i in locations
    ]

    df["lon"] = [
     india_farm_locations[i][1]
     + np.random.uniform(-0.5, 0.5)
     for i in locations
    ]

    temperatures = []
    humidities = []
    rainfalls = []

    for lat, lon in zip(df["lat"], df["lon"]):

        weather = get_weather(lat, lon)

        temperatures.append(weather["temperature"])
        humidities.append(weather["humidity"])
        rainfalls.append(weather["rainfall"])

    df["temperature"] = temperatures
    df["humidity"] = humidities
    df["rainfall"] = rainfalls

    # -----------------------------
    # Add Time-Series NDVI
    # -----------------------------
    # Simulates previous week's NDVI

    df["ndvi_last_week"] = (
        df["ndvi"] -
        np.random.uniform(-0.1, 0.1, len(df))
    )

    # -----------------------------
    # NDVI Trend
    # -----------------------------
    # Positive -> improving crop health
    # Negative -> declining crop health

    df["ndvi_trend"] = (
        df["ndvi"] -
        df["ndvi_last_week"]
    )

    return df