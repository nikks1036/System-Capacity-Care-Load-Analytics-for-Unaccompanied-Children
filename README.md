# 📊 System-Capacity-Care-Load-Analytics-for-Unaccompanied-Children

## 📌 Project Overview
This project analyzes the care system load for Unaccompanied Children (UAC). It helps monitor system capacity, understand trends, and predict future care demand using data analytics and machine learning.

## 🎯 Objectives
- Analyze total system load (CBP + HHS)
- Monitor intake vs discharge trends
- Identify system stress periods
- Predict future care load using machine learning

## 🔄 System Workflow
CBP Custody → Transfer to HHS → Care → Discharge to Sponsor

## 📊 Features
- 📈 Interactive Dashboard (Streamlit)
- 📊 KPI Metrics (Total Load, Net Intake, etc.)
- 📉 Trend Analysis (Daily, Weekly)
- 🤖 Prediction Model (Future Load Forecast)
- 🎨 Professional UI (Tabs, Filters, Styled Layout)

## 🧮 Key Metrics
- **Total System Load** = CBP Custody + HHS Care
- **Net Intake** = Transferred - Discharged
- **Rolling Average** = Trend Analysis
- **Backlog Indicator** = Continuous intake pressure

## 🤖 Machine Learning
- Model Used: Linear Regression
- Purpose: Predict future system load for next 30 days
- 
## 🛠️ Tech Stack
- Python
- Pandas
- Streamlit
- Plotly
- Scikit-learn

## 📂 Project Structure
```bash
UAC_Care_Analytics/
│
├── app/
│ └── streamlit_app.py
│
├── data/
│ └── uac_data.csv
│
├── utils/
│ └── metrics.py
│
├── notebooks/
│ └── eda_analysis.ipynb
│
└── README.md

