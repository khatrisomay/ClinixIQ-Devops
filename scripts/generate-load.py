import argparse
import random
import sys
import time
import urllib.request
import json

CONDITIONS = [
    {"symptoms": "severe chest tightness and sudden shortness of breath", "temp": 98.6, "hr": 115, "o2": 89},
    {"symptoms": "scratchy throat, persistent dry cough, runny nose", "temp": 99.8, "hr": 78, "o2": 99},
    {"symptoms": "throbbing headache on right temple with extreme light sensitivity", "temp": 98.4, "hr": 82, "o2": 98},
    {"symptoms": "watery diarrhea, severe abdominal cramps, low grade fever", "temp": 100.8, "hr": 92, "o2": 97},
    {"symptoms": "stiff neck, high fever, unbearable headache, confusion", "temp": 103.5, "hr": 128, "o2": 93},
]

def send_request(base_url: str):
    profile = random.choice(CONDITIONS)
    payload = json.dumps({
        "symptoms": profile["symptoms"],
        "temperature": profile["temp"] + random.uniform(-0.5, 0.5),
        "heart_rate": int(profile["hr"] + random.randint(-5, 10)),
        "oxygen_level": int(profile["o2"] + random.randint(-2, 1)),
        "duration_days": random.randint(1, 5)
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{base_url}/api/v1/triage/predict",
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "ClinixIQ-Chaos-LoadGen/1.0"}
    )
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            latency = (time.time() - start) * 1000
            return response.status, latency
    except Exception as e:
        latency = (time.time() - start) * 1000
        return 500, latency

def main():
    parser = argparse.ArgumentParser(description="ClinixIQ Chaos & Telemetry Load Generator")
    parser.add_argument("--url", default="http://localhost:8000", help="Base backend URL")
    parser.add_argument("--requests", type=int, default=100, help="Total requests to dispatch")
    parser.add_argument("--delay", type=float, default=0.05, help="Delay between requests in seconds")
    args = parser.parse_args()

    print(f"==> Initiating synthetic clinical load on {args.url} ({args.requests} requests)...")
    successes, failures = 0, 0
    latencies = []

    for i in range(1, args.requests + 1):
        status, lat = send_request(args.url)
        latencies.append(lat)
        if status == 200:
            successes += 1
        else:
            failures += 1

        if i % 20 == 0 or i == args.requests:
            avg_lat = sum(latencies[-20:]) / len(latencies[-20:])
            print(f"[{i}/{args.requests}] Sent | Success: {successes} | Fail: {failures} | Rolling Avg Latency: {avg_lat:.2f}ms")
        time.sleep(args.delay)

    p95 = sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0
    print("\n==========================================================")
    print("   Load Generation Summary Results                        ")
    print("==========================================================")
    print(f"Total Requests  : {args.requests}")
    print(f"Successful (200): {successes}")
    print(f"Failed (5xx)    : {failures}")
    print(f"P95 Latency     : {p95:.2f}ms")
    print(f"Mean Latency    : {sum(latencies)/len(latencies):.2f}ms")
    print("==========================================================")

if __name__ == "__main__":
    main()
