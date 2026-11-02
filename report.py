import pandas as pd
import matplotlib.pyplot as plt

from parser import parse_log_file

events = parse_log_file("sample_auth.log")
df = pd.DataFrame(events)

# Keep only failed logins and add an "hour" column
failed = df[df["status"] == "Failed"].copy()
failed["hour"] = failed["timestamp"].dt.hour

# Chart 1: failed logins per hour of the day
per_hour = failed.groupby("hour").size().reindex(range(24), fill_value=0)

plt.figure(figsize=(10, 5))
per_hour.plot(kind="bar", color="crimson")
plt.title("Failed Logins per Hour")
plt.xlabel("Hour of day (0-23)")
plt.ylabel("Failed attempts")
plt.tight_layout()
plt.savefig("failed_per_hour.png")
plt.close()

# Chart 2: top 5 IPs by failed attempts
top_ips = failed["ip"].value_counts().head(5)

plt.figure(figsize=(8, 5))
top_ips.sort_values().plot(kind="barh", color="steelblue")
plt.title("Top 5 IPs by Failed Attempts")
plt.xlabel("Failed attempts")
plt.ylabel("IP address")
plt.tight_layout()
plt.savefig("top_ips.png")
plt.close()

print("Saved failed_per_hour.png and top_ips.png")