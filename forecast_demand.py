import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# 1. Connect and Fetch Data
db_connection_str = 'mysql+mysqlconnector://root:1234@127.0.0.1/SupplyChain'
db_connection = create_engine(db_connection_str)

print("Fetching data...")
query = """
SELECT 
    order_date_dateorders as date,
    SUM(order_item_quantity) as total_quantity
FROM 
    raw_supply_chain_data
GROUP BY 
    order_date_dateorders;
"""
df = pd.read_sql(query, db_connection)

# 2. Prep Data (Group by Month)
df['date'] = pd.to_datetime(df['date'], format='mixed')
df.set_index('date', inplace=True)
monthly_data = df.resample('ME').sum() # Resample to Month End
# Fill missing months with 0 to prevent errors
monthly_data = monthly_data.fillna(0)

# 3. Train the Model (Holt-Winters Exponential Smoothing)
# This model learns the "Trend" and "Seasonality" automatically
print("Training prediction model...")
model = ExponentialSmoothing(
    monthly_data['total_quantity'], 
    trend='add', 
    seasonal='add', 
    seasonal_periods=12
).fit()

# 4. Predict the next 6 Months
forecast = model.forecast(6)

print("\n--- FUTURE INVENTORY NEEDS ---")
print(forecast)

# 5. Visualize History vs Forecast
plt.figure(figsize=(14, 7))

# Plot History
plt.plot(monthly_data.index, monthly_data['total_quantity'], label='Actual Sales History', marker='o')

# Plot Forecast
plt.plot(forecast.index, forecast, label='AI Forecast (Next 6 Months)', color='red', linestyle='--', marker='x', linewidth=2)

plt.title('Supply Chain Forecast: Actual vs Predicted Demand')
plt.xlabel('Date')
plt.ylabel('Quantity Needed')
plt.legend()
plt.grid(True)
plt.show()