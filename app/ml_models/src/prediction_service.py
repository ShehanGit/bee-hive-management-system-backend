import pandas as pd
import joblib
import numpy as np
from feature_engineering import engineer_features

def predict_honey_production(input_data: pd.DataFrame, model_path="random_forest_model.pkl"):
    """
    Given a DataFrame with new candidate locations (and necessary features),
    return the predicted honey production from the trained Random Forest model.
    """
    # Load model
    model = joblib.load(model_path)
    
    # Make sure input data has the correct features
    input_data_fe = engineer_features(input_data)
    
    # Get expected feature names from the trained model
    expected_features = model.feature_names_in_
    
    # Ensure the new input data has the same features as the model
    for col in expected_features:
        if col not in input_data_fe.columns:
            input_data_fe[col] = 0  # Add missing columns with default value
    
    # Reorder columns to match training set
    input_data_fe = input_data_fe[expected_features]
    
    # Predict honey production
    predictions = model.predict(input_data_fe)
    return predictions

if __name__ == "__main__":
    # Example: New hive candidate locations (ensure all necessary features are included)
    new_data = pd.DataFrame({
        'hive_lat': [7.2914],  # Single hive location
        'hive_lng': [80.6337],
        'dist_to_water_source': [3.4],
        'dist_to_feeding_station': [1.5],
        'dist_to_flowering_area': [3.0],
        'humidity': [65],
        'temperature': [32]
    })

    predicted_values = predict_honey_production(new_data, "random_forest_model.pkl")
    print("Predicted honey production for new locations:", predicted_values)
