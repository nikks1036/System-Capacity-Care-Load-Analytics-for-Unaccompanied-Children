import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="UAC Care Analytics", layout="wide")


st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(to right, #eef2f3, #dfe9f3);
}

/* KPI Cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    color: white;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 3px 3px 12px rgba(0,0,0,0.2);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #1f4037, #99f2c8);
    color: white;
}

/* Titles */
h1, h2, h3 {
    color: #1f4e79;
    font-weight: bold;
}

/* Buttons */
button {
    border-radius: 10px !important;
}

/* Tables */
.dataframe {
    border-collapse: collapse;
    border-radius: 10px;
    overflow: hidden;
}
.dataframe th {
    background-color: #2575fc;
    color: white;
}
.dataframe td {
    background-color: #f9f9f9;
}

/* Tabs */
.stTabs [role="tab"] {
    font-size: 16px;
    padding: 10px;
}
.stTabs [aria-selected="true"] {
    background-color: #2575fc !important;
    color: white !important;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.title("📊 System Capacity & Care Load Analytics for Unaccompanied Children")

st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    h1, h2, h3 {
        color: #1f4e79;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv(r"D:\UAC_Care_Analytices\data\uac_data.csv")

# Fix Date
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
df = df.dropna(subset=["Date"])

# Rename columns
df.columns = [
    "Date",
    "CBP_Apprehended",
    "CBP_Custody",
    "Transferred_to_HHS",
    "HHS_Care",
    "HHS_Discharged"
]

# Convert numeric
numeric_cols = [
    "CBP_Apprehended",
    "CBP_Custody",
    "Transferred_to_HHS",
    "HHS_Care",
    "HHS_Discharged"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.fillna(0)
df = df.sort_values("Date")

# -----------------------------
# METRICS
# -----------------------------
df["Total_System_Load"] = df["CBP_Custody"] + df["HHS_Care"]
df["Net_Intake"] = df["Transferred_to_HHS"] - df["HHS_Discharged"]
df["Load_7day"] = df["Total_System_Load"].rolling(7).mean()
df["Load_14day"] = df["Total_System_Load"].rolling(14).mean()


# -----------------------------
# PREDICTION MODEL
# -----------------------------
from sklearn.linear_model import LinearRegression
import numpy as np

df_pred = df.copy()
df_pred["Days"] = (df_pred["Date"] - df_pred["Date"].min()).dt.days

X = df_pred[["Days"]]
y = df_pred["Total_System_Load"]

model = LinearRegression()
model.fit(X, y)

future_days = np.arange(df_pred["Days"].max()+1, df_pred["Days"].max()+31)
future_df = pd.DataFrame({"Days": future_days})

future_df["Predicted_Load"] = model.predict(future_df)

future_df["Date"] = df_pred["Date"].max() + pd.to_timedelta(
    future_days - df_pred["Days"].max(), unit="D"
)
# -----------------------------
# SIDEBAR FILTER
# -----------------------------
st.sidebar.header("🔍 Filters")

start = st.sidebar.date_input("Start Date", df["Date"].min().date())
end = st.sidebar.date_input("End Date", df["Date"].max().date())

filtered = df[
    (df["Date"] >= pd.to_datetime(start)) &
    (df["Date"] <= pd.to_datetime(end))
]

# -----------------------------
# KPI SECTION
# -----------------------------
# -----------------------------
# KPI SECTION WITH COLORS
# -----------------------------
st.subheader("📌 Key Performance Indicators")

# KPI values
total_load_val = int(filtered["Total_System_Load"].mean())
net_intake_val = int(filtered["Net_Intake"].mean())
max_load_val = int(filtered["Total_System_Load"].max())
min_load_val = int(filtered["Total_System_Load"].min())

# Custom HTML for colored cards
kpi_html = f"""
<div style="display: flex; gap: 20px; margin-bottom: 20px;">
    <div style="background: linear-gradient(to right, #6a11cb, #2575fc); padding: 20px; border-radius: 12px; flex: 1; text-align: center; color:white; box-shadow: 2px 2px 10px rgba(0,0,0,0.2);">
        <h4>📊 Total Load</h4>
        <h2>{total_load_val}</h2>
    </div>
    <div style="background: linear-gradient(to right, #ff416c, #ff4b2b); padding: 20px; border-radius: 12px; flex: 1; text-align: center; color:white; box-shadow: 2px 2px 10px rgba(0,0,0,0.2);">
        <h4>⚖ Net Intake</h4>
        <h2>{net_intake_val}</h2>
    </div>
    <div style="background: linear-gradient(to right, #00c6ff, #0072ff); padding: 20px; border-radius: 12px; flex: 1; text-align: center; color:white; box-shadow: 2px 2px 10px rgba(0,0,0,0.2);">
        <h4>📈 Max Load</h4>
        <h2>{max_load_val}</h2>
    </div>
    <div style="background: linear-gradient(to right, #f7971e, #ffd200); padding: 20px; border-radius: 12px; flex: 1; text-align: center; color:white; box-shadow: 2px 2px 10px rgba(0,0,0,0.2);">
        <h4>📉 Min Load</h4>
        <h2>{min_load_val}</h2>
    </div>
</div>
"""

st.markdown(kpi_html, unsafe_allow_html=True)
# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Analysis", "📉 Trends", "🤖 Prediction"])

# -----------------------------
# TAB 1: OVERVIEW
# -----------------------------
with tab1:
    st.subheader("Total System Load Over Time")
    fig1 = px.line(filtered, x="Date", y="Total_System_Load")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("CBP vs HHS Load")
    fig2 = px.line(filtered, x="Date",
                   y=["CBP_Custody", "HHS_Care"])
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# TAB 2: ANALYSIS
# -----------------------------
with tab2:
    st.subheader("📊 Data Table")

    st.dataframe(filtered.style
        .background_gradient(cmap="Blues")
        .highlight_max(axis=0, color="lightgreen")
        .highlight_min(axis=0, color="salmon")
    )
# -----------------------------
# TAB 3: TRENDS
# -----------------------------
with tab3:
    st.subheader("Rolling Average Trends")
    fig5 = px.line(filtered, x="Date",
                   y=["Load_7day", "Load_14day"])
    st.plotly_chart(fig5, use_container_width=True)
    
# -----------------------------
# TAB 4: PREDICTION
# -----------------------------
with tab4:
    st.subheader("Future Load Prediction (Next 30 Days)")

    fig6 = px.line(future_df, x="Date", y="Predicted_Load")
    st.plotly_chart(fig6, use_container_width=True)
    
# -----------------------------
# INSIGHTS (ADD HERE)
# -----------------------------
st.markdown("## 📌 Key Insights")

avg_load = int(df["Total_System_Load"].mean())
max_load = int(df["Total_System_Load"].max())
min_load = int(df["Total_System_Load"].min())

st.write(f"""
- 📊 Average system load is **{avg_load} children**
- 🔺 Peak load reached **{max_load} children**
- 🔻 Minimum load observed was **{min_load} children**
- ⚖ Positive Net Intake indicates system stress periods
- 📉 Rolling averages show trend patterns over time
""")