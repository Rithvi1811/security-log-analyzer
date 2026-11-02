import random
from datetime import datetime, timedelta

random.seed(42)  # same output every run

users = ["alice", "bob", "charlie", "dave"]
normal_ips = ["10.0.0.5", "10.0.0.8", "10.0.0.12", "10.0.0.20"]
attack_users = ["admin", "root", "test", "guest", "oracle"]
attacker_ip = "203.0.113.45"

start = datetime(2026, 11, 1)
events = []

# Normal activity: mostly successful logins, a few typos
for _ in range(300):
    t = start + timedelta(seconds=random.randint(0, 86400))
    status = random.choices(["Accepted", "Failed"], weights=[90, 10])[0]
    events.append((t, status, random.choice(users), random.choice(normal_ips)))

# Attack: 40 failed attempts, one every 3 seconds
attack_start = start + timedelta(hours=3, minutes=12)
for i in range(40):
    t = attack_start + timedelta(seconds=i * 3)
    events.append((t, "Failed", random.choice(attack_users), attacker_ip))

events.sort(key=lambda e: e[0])

with open("sample_auth.log", "w") as f:
    for t, status, user, ip in events:
        f.write(f"{t:%Y-%m-%d %H:%M:%S} {status} password for {user} from {ip}\n")

print(f"Wrote {len(events)} log lines to sample_auth.log")