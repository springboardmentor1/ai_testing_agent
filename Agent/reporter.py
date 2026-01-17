import json
from datetime import datetime

def generate_report(status):
    report = {
        "status": status,
        "time": str(datetime.now())
    }
    with open("test_report.json", "w") as f:
        json.dump(report, f, indent=2)
