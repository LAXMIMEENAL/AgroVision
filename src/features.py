import numpy as np


def create_features(df):

    # ---------------------------------
    # Binary Risk Indicators
    # ---------------------------------

    # Low vegetation health
    df["low_ndvi"] = (
        df["ndvi"] < 0.4
    ).astype(int)

    # Low rainfall condition
    df["low_rain"] = (
        df["rainfall"] < 50
    ).astype(int)

    # High temperature stress
    df["high_temp"] = (
        df["temperature"] > 35
    ).astype(int)

    # Poor soil health
    df["poor_soil"] = (
        (df["N"] < 40) |
        (df["P"] < 40) |
        (df["K"] < 40)
    ).astype(int)

    # ---------------------------------
    # NDVI Trend Feature
    # ---------------------------------

    # Crop health improving or declining
    df["declining_ndvi"] = (
        df["ndvi_trend"] < -0.05
    ).astype(int)

    # ---------------------------------
    # Risk Score Calculation
    # ---------------------------------

    # Weighted risk score (0 - 100)

    df["risk_score"] = (
        df["low_ndvi"] * 35 +
        df["low_rain"] * 25 +
        df["high_temp"] * 20 +
        df["poor_soil"] * 10 +
        df["declining_ndvi"] * 10
    )

    # ---------------------------------
    # Risk Level Classification
    # ---------------------------------

    def classify_risk(score):

        if score >= 70:
            return "High"

        elif score >= 40:
            return "Medium"

        else:
            return "Low"

    df["risk_level"] = (
        df["risk_score"]
        .apply(classify_risk)
    )

    return df