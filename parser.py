import re
from collections import Counter
from datetime import datetime

LOG_PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"(Accepted|Failed) password for (\w+) from ([\d.]+)$"
)

def parse_line(line):
    """Return a dict for a valid log line, or None if it doesn't match."""
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None
    timestamp, status, user, ip = match.groups()
    return {
        "timestamp": datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
        "status": status,
        "user": user,
        "ip": ip,
    }

def parse_log_file(path):
    events = []
    with open(path) as f:
        for line in f:
            event = parse_line(line)
            if event:
                events.append(event)
    return events

if __name__ == "__main__":
    events = parse_log_file("sample_auth.log")
    failed = [e for e in events if e["status"] == "Failed"]

    print(f"Total events parsed: {len(events)}")
    print(f"Failed logins: {len(failed)}")
    print("Top IPs by failed attempts:")
    for ip, count in Counter(e["ip"] for e in failed).most_common(5):
        print(f"  {ip}: {count}")