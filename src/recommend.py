def recommend(row):

    recommendations = []

    # ---------------------------------
    # NDVI-based Recommendation
    # ---------------------------------

    if row["low_ndvi"]:
        recommendations.append(
            "Improve crop health using fertilizer or pest control"
        )

    # ---------------------------------
    # Rainfall-based Recommendation
    # ---------------------------------

    if row["low_rain"]:
        recommendations.append(
            "Increase irrigation due to low rainfall"
        )

    # ---------------------------------
    # Temperature-based Recommendation
    # ---------------------------------

    if row["high_temp"]:
        recommendations.append(
            "Use heat-resistant crops or mulching techniques"
        )

    # ---------------------------------
    # Soil-based Recommendation
    # ---------------------------------

    if row["poor_soil"]:
        recommendations.append(
            "Improve soil nutrients (NPK balance)"
        )

    # ---------------------------------
    # NDVI Trend Recommendation
    # ---------------------------------

    if row["declining_ndvi"]:
        recommendations.append(
            "Crop health is declining — inspect for disease or water stress"
        )

    # ---------------------------------
    # Risk-Level Based Recommendation
    # ---------------------------------

    if row["risk_level"] == "High":
        recommendations.append(
            "Immediate agricultural intervention recommended"
        )

    # ---------------------------------
    # Safe Condition
    # ---------------------------------

    if len(recommendations) == 0:
        recommendations.append(
            "Farm conditions are healthy"
        )

    # ---------------------------------
    # Combine Recommendations
    # ---------------------------------

    return " | ".join(recommendations)