 📦 Supply Chain Analytics & AI Demand Forecasting

 📊 Project Overview
This project analyzes 180,000+ supply chain records to identify shipping bottlenecks and predict future inventory demand. 

By combining SQL for rootcause analysis and Python (Machine Learning) for forecasting, I discovered a critical shipping failure in Central America and built a demand model that successfully adapted to a volatile market shift.

Key Technologies: `MySQL`, `Python`, `Pandas`, `Statsmodels`, `Matplotlib`, `SQLAlchemy`



 🚀 Key Business Insights

 1. The "Premium Shipping" Trap
I investigated why highpriority shipments were consistently late in the Central America region.
 Hypothesis: Faster shipping modes (First Class) should have lower delay rates.
 Data Reality:  Standard Class: 38% Late Rate (Reliable)
     First Class: 95.5% Late Rate (Critical Failure)
 Recommendation: Immediate suspension of "First Class" upgrades for this region, as the premium service is failing 95% of the time.

(<img width="494" height="133" alt="image" src="https://github.com/user-attachments/assets/fe49b5c5-2c1e-4d2a-952f-fc0853567ac1" />
)
(Table showing the 95% failure rate for First Class shipping)

 2. The Bottleneck Product
I identified that a single product, the "Perfect Fitness Perfect Rip Deck", was responsible for a disproportionate number of customer complaints, specifically when shipped to Central American distribution centers.



 🧠 AI Demand Forecasting
Moving from diagnosing the past to predicting the future, I built a timeseries forecasting pipeline using HoltWinters Exponential Smoothing.

 The Challenge: The dataset contained a massive drop in sales volume in late 2017 (a "regime change" in the data).
 The Solution: The AI model correctly identified this downward trend and adjusted its predictions for the next 6 months, avoiding the common mistake of overpredicting based on historical highs.

(<img width="1919" height="909" alt="image" src="https://github.com/user-attachments/assets/496b60ec-98d2-4a86-b896-c34f94b74b95" />
)
(The Red line shows the AI adapting to the sudden drop in sales history)



 💻 Technical Implementation

 1. Automated ETL Pipeline (`import_data.py`)
Instead of manual entry, I built a Python script to ingest raw CSV data into MySQL.
 Features: Handles 180k rows using chunking to prevent server timeouts.
 Sanitization: Automatically cleans column names and handles encoding errors.

 2. The SQL Analysis
The core analysis relied on complex aggregations and filtering. Here is the query used to find the "Bad Apple" shipping mode:

```sql
SELECT 
    shipping_mode,
    COUNT() as total_orders,
    SUM(CASE WHEN delivery_status = 'Late delivery' THEN 1 ELSE 0 END) as late_count,
    ROUND((SUM(CASE WHEN delivery_status = 'Late delivery' THEN 1 ELSE 0 END) / COUNT())  100, 2) as late_percentage
FROM raw_supply_chain_data
WHERE order_region = 'Central America'
GROUP BY shipping_mode
ORDER BY late_percentage ASC;
