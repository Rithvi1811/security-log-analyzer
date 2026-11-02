import pandas as pd
import streamlit as st

from parser import parse_log_file
from detector import find_brute_force

st.set_page_config(page_title="Security Log Analyzer", layout="wide")
st.title("🛡️ Security Log Analyzer")

events = parse_log_file("sample_auth.log")
df = pd.DataFrame(events)
failed = df[df["status"] == "Failed"].copy()
alerts = find_brute_force(events)

# Summary numbers at the top
col1, col2, col3 = st.columns(3)
col1.metric("Total events", len(df))
col2.metric("Failed logins", len(failed))
col3.metric("Alerts raised", len(alerts))

# Alerts table
st.subheader("Alerts")
if alerts:
    st.dataframe(pd.DataFrame(alerts))
else:
    st.success("No suspicious activity detected.")

# Charts
failed["hour"] = failed["timestamp"].dt.hour
per_hour = failed.groupby("hour").size().reindex(range(24), fill_value=0)

st.subheader("Failed logins per hour")
st.bar_chart(per_hour)

st.subheader("Top IPs by failed attempts")
st.bar_chart(failed["ip"].value_counts().head(5))