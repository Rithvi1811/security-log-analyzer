# 🛡️ Security Log Analyzer

A Python tool that analyzes server login logs, automatically detects brute-force attacks, and shows the results in an interactive dashboard.

## What it does

- Parses authentication logs using regular expressions
- Detects brute-force attacks (5+ failed logins from one IP within 2 minutes) using a sliding-window algorithm
- Reports the attacker's IP, the usernames tried, and the time range
- Visualizes failed logins per hour and top offending IPs
- Presents everything in a Streamlit dashboard

## Tech stack

Python, pandas, matplotlib, Streamlit, regex

## Project files

| File | Purpose |
|------|---------|
| `generate_logs.py` | Creates sample log data with a simulated attack |
| `parser.py` | Turns raw log lines into structured data |
| `detector.py` | Brute-force detection logic |
| `report.py` | Generates static charts |
| `app.py` | Streamlit dashboard |

## How to run

```bash
git clone https://github.com/Rithvi1811/security-log-analyzer.git
cd security-log-analyzer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python generate_logs.py
streamlit run app.py
```

## What I learned

- Parsing text data with regex
- Sliding-window detection logic
- Data analysis with pandas
- Building dashboards with Streamlit
- Using Git and GitHub

*All data is simulated for learning purposes.*


   🔗 **Live demo:** https://security-log-analyzer-zdvfxnu6farifq2cwfiewa.streamlit.app