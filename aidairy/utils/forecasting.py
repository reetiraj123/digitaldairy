"""
Forecasting utility module for SmartDairy
Implements simple moving average forecasting for milk quantity prediction
"""

import pandas as pd
import numpy as np
from typing import List, Tuple, Optional
from datetime import datetime, timedelta
from utils.db import get_customer_entries_for_forecast

def calculate_moving_average(values: List[float], window: int = 7) -> float:
    """
    Calculate moving average of the last N values
    Default window is 7 days
    """
    if len(values) == 0:
        return 0.0
    
    if len(values) < window:
        # If we have fewer values than window, use all available
        return sum(values) / len(values)
    
    # Return average of last 'window' values
    return sum(values[-window:]) / window

def predict_next_day_quantity(customer_id: int, window: int = 7) -> Tuple[float, List[Tuple[str, float]]]:
    """
    Predict next day's milk quantity for a customer using moving average
    Returns: (predicted_quantity, historical_data)
    """
    # Get recent entries (last 30 days)
    entries = get_customer_entries_for_forecast(customer_id, days=30)
    
    if len(entries) == 0:
        return 0.0, []
    
    # Extract quantities in chronological order (oldest first)
    entries_sorted = sorted(entries, key=lambda x: x[0])
    quantities = [entry[1] for entry in entries_sorted]
    dates = [entry[0] for entry in entries_sorted]
    
    # Calculate moving average
    predicted = calculate_moving_average(quantities, window)
    
    # Prepare historical data for visualization
    historical_data = [(date, qty) for date, qty in zip(dates, quantities)]
    
    return predicted, historical_data

def get_forecast_dataframe(customer_id: int, window: int = 7) -> pd.DataFrame:
    """
    Get forecast data as a pandas DataFrame for visualization
    """
    predicted, historical = predict_next_day_quantity(customer_id, window)
    
    if len(historical) == 0:
        return pd.DataFrame()
    
    # Create DataFrame with historical data
    df = pd.DataFrame(historical, columns=['Date', 'Quantity'])
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Add predicted value for next day
    if len(df) > 0:
        last_date = df['Date'].max()
        next_date = last_date + timedelta(days=1)
        predicted_row = pd.DataFrame({
            'Date': [next_date],
            'Quantity': [predicted]
        })
        df = pd.concat([df, predicted_row], ignore_index=True)
    
    return df

def get_forecast_summary(customer_id: int, window: int = 7) -> dict:
    """
    Get forecast summary with statistics
    """
    predicted, historical = predict_next_day_quantity(customer_id, window)
    
    if len(historical) == 0:
        return {
            'predicted_quantity': 0.0,
            'historical_avg': 0.0,
            'historical_min': 0.0,
            'historical_max': 0.0,
            'data_points': 0
        }
    
    quantities = [h[1] for h in historical]
    
    return {
        'predicted_quantity': round(predicted, 2),
        'historical_avg': round(sum(quantities) / len(quantities), 2),
        'historical_min': round(min(quantities), 2),
        'historical_max': round(max(quantities), 2),
        'data_points': len(historical),
        'window_size': window
    }

