from collections import defaultdict
from datetime import timedelta

from parser import parse_log_file

FAIL_THRESHOLD = 5               # failures needed to raise an alert
WINDOW = timedelta(minutes=2)    # ...within this much time


def find_brute_force(events):
    """Return a list of alerts for IPs with too many failures in a short window."""
    # 1. Group failed attempts by IP address
    failed_by_ip = defaultdict(list)
    for event in events:
        if event["status"] == "Failed":
            failed_by_ip[event["ip"]].append(event)

    alerts = []

    # 2. For each IP, slide a 2-minute window across its attempts
    for ip, attempts in failed_by_ip.items():
        attempts.sort(key=lambda e: e["timestamp"])
        start = 0
        best_window = []

        for end in range(len(attempts)):
            # shrink the window from the left until it fits in 2 minutes
            while attempts[end]["timestamp"] - attempts[start]["timestamp"] > WINDOW:
                start += 1
            window = attempts[start:end + 1]
            if len(window) > len(best_window):
                best_window = window

        # 3. Raise an alert if the busiest window crosses the threshold
        if len(best_window) >= FAIL_THRESHOLD:
            alerts.append({
                "ip": ip,
                "failures": len(best_window),
                "users_tried": sorted({e["user"] for e in best_window}),
                "first_seen": best_window[0]["timestamp"],
                "last_seen": best_window[-1]["timestamp"],
            })

    return alerts


if __name__ == "__main__":
    events = parse_log_file("sample_auth.log")
    alerts = find_brute_force(events)

    print("=== SECURITY REPORT ===")
    if not alerts:
        print("No suspicious activity detected.")
    for a in alerts:
        print(f"\n[ALERT] Possible brute-force attack from {a['ip']}")
        print(f"  Failed logins in window: {a['failures']}")
        print(f"  Usernames tried: {', '.join(a['users_tried'])}")
        print(f"  Time: {a['first_seen']} to {a['last_seen']}")