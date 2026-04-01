import pandas as pd

def compute_metrics(df):

    df["Total_System_Load"] = df["CBP_Custody"] + df["HHS_Care"]

    df["Net_Intake"] = df["Transferred_to_HHS"] - df["HHS_Discharged"]

    df["Care_Load_Growth"] = df["Total_System_Load"].pct_change() * 100

    df["Backlog"] = df["Net_Intake"].rolling(7).sum()

    df["Load_7day"] = df["Total_System_Load"].rolling(7).mean()

    df["Load_14day"] = df["Total_System_Load"].rolling(14).mean()

    df["Discharge_Ratio"] = df["HHS_Discharged"] / df["Transferred_to_HHS"]

    return df


def kpi_summary(df):

    kpis = {
        "Total Children Under Care": int(df["Total_System_Load"].mean()),
        "Net Intake Pressure": int(df["Net_Intake"].mean()),
        "Care Load Volatility": float(df["Total_System_Load"].std()),
        "Backlog Rate": float(df["Backlog"].mean()),
        "Discharge Ratio": float(df["Discharge_Ratio"].mean())
    }

    return kpis