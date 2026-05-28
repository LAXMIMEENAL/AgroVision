def get_feature_importance(model):
    return dict(zip(
        ["ndvi", "rainfall", "temperature"],
        model.feature_importances_
    ))