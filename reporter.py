import time
from datetime import datetime

def create_report(test_case, steps, status, error=None, start_time=None):
    end_time = time.time()

    return {
        "test_case": test_case,
        "status": status,
        "steps_executed": len(steps),
        "error": str(error) if error else None,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "execution_time_sec": round(end_time - start_time, 2) if start_time else None
    }
