import streamlit as st
import pickle
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from streamlit_autorefresh import st_autorefresh

from src.data_loader import load_data
from src.features import create_features
from src.model import  train_model
from src.recommend import recommend
from src.timeseries import generate_ndvi_series, detect_trend
from src.explain import get_feature_importance
from src.model import (
    train_model,
    get_feature_importance
)
st.title("🌾 Farm Risk Intelligence System")

# Load data
df = load_data()
df = create_features(df)



# ---------------------------------
# SIDEBAR FILTERS
# ---------------------------------

st.sidebar.header("🔍 Filters")

selected_risk = st.sidebar.multiselect(
    "Select Risk Level",
    options=df["risk_level"].unique(),
    default=df["risk_level"].unique()
)

df = df[
    df["risk_level"].isin(selected_risk)
]
# Train model
model = train_model(df)

# Predictions
# ---------------------------------
# MODEL PREDICTIONS
# ---------------------------------

feature_columns = [
    "ndvi",
    "rainfall",
    "temperature",
    "humidity",
    "N",
    "P",
    "K",
    "ph",
    "ndvi_trend"
]

X = df[feature_columns]

df["predicted_risk"] = model.predict(X)
# Recommendations
df["recommendation"] = df.apply(recommend, axis=1)

# Show table
st.write(df.head())




tab1, tab2, tab3 = st.tabs([
    "🗺️ GeoAI Dashboard",
    "📈 Analytics",
    "🤖 Recommendations"
])


# Map
with tab1:

    st.subheader("🗺️ Risk Map")
    m = folium.Map(
        location=[20, 78],
        zoom_start=5
    )

    marker_cluster = MarkerCluster().add_to(m)

    sample_df = df

    for _, row in sample_df.iterrows():

        color = "green"

        if row["risk_score"] >= 70:
            color = "red"

        elif row["risk_score"] >= 40:
            color = "orange"

        folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=3,
        color=color,
        fill=True,
        fill_color=color,
        popup=f"""
        Risk Score: {row['risk_score']}
        <br>
        Risk Level: {row['risk_level']}
        """
    ).add_to(marker_cluster)

    st_folium(m)
    st.markdown("""
### 🗺️ Map Density Legend

- 🟢 Green → Low farm density
- 🟡 Yellow/Orange → Medium farm density
- 🔴 Red → High farm density
""")

with tab2:
    st.subheader("📈 Risk Distribution")

    risk_counts = df["risk_level"].value_counts()

    st.pyplot(
        risk_counts.plot.pie(
        autopct="%1.1f%%",
        figsize=(5, 5)
    ).figure
    )



    st.subheader("🌦️ Live Weather Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
       "Avg Temperature",
    f"{df['temperature'].mean():.1f} °C"
    )

    col2.metric(
       "Avg Humidity",
    f"{df['humidity'].mean():.1f} %"
    )

    col3.metric(
    "Avg Rainfall",
    f"{df['rainfall'].mean():.1f} mm",
    help="Live rainfall from OpenWeatherMap API"
    )


# Time-series
    st.subheader("📈 NDVI Trend")
    series = generate_ndvi_series()
    trend = detect_trend(series)

    st.line_chart(series)
    st.write("Trend:", trend)

# Feature importance
    st.subheader("🧠 Feature Importance")

    importance = get_feature_importance(
    model,
    feature_columns
    )

    importance_df = pd.DataFrame({
    "Feature": importance.keys(),
    "Importance": importance.values()
    })

    st.dataframe(
    importance_df.sort_values(
        by="Importance",
        ascending=False
    )
    )
with tab3:
# Alerts
    st.subheader("🚨 Alerts")
    high_risk = df[df["risk_score"] > 70]
    if not high_risk.empty:
       st.warning("High risk farms detected!")

# Recommendations
    st.subheader("📌 Recommendations")
    st.write(df[["risk_score", "recommendation"]].head())

    st_autorefresh(
    interval=60000,
    key="farm_dashboard_refresh"
    )