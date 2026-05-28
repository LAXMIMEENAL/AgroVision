from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    r2_score
)

import pickle


def train_model(df):

    # ---------------------------------
    # Input Features
    # ---------------------------------

    X = df[[
        "ndvi",
        "rainfall",
        "temperature",
        "humidity",
        "N",
        "P",
        "K",
        "ph",
        "ndvi_trend"
    ]]

    # ---------------------------------
    # Target Variable
    # ---------------------------------

    y = df["risk_score"]

    # ---------------------------------
    # Train-Test Split
    # ---------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # ---------------------------------
    # Model Initialization
    # ---------------------------------

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    # ---------------------------------
    # Model Training
    # ---------------------------------

    model.fit(X_train, y_train)

    # ---------------------------------
    # Predictions
    # ---------------------------------

    predictions = model.predict(X_test)

    # ---------------------------------
    # Evaluation Metrics
    # ---------------------------------

    mae = mean_absolute_error(y_test, predictions)

    r2 = r2_score(y_test, predictions)

    print("\nModel Performance")
    print("-------------------")
    print(f"MAE Score : {mae:.2f}")
    print(f"R2 Score  : {r2:.2f}")

    # ---------------------------------
    # Save Model
    # ---------------------------------

    with open("models/model.pkl", "wb") as f:
        pickle.dump(model, f)

    return model


# ---------------------------------
# Prediction Function
# ---------------------------------

def predict_risk(model, input_data):

    prediction = model.predict(input_data)

    return prediction


# ---------------------------------
# Feature Importance
# ---------------------------------

def get_feature_importance(model, feature_names):

    importance = model.feature_importances_

    feature_importance = dict(
        zip(feature_names, importance)
    )

    return feature_importance