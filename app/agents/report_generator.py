import datetime

def generate_report(instruction, actions, execution):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = {
        "test_summary": {
            "instruction": instruction,
            "total_steps": len(actions),
            "status": execution["status"],
            "executed_at": timestamp
        },
        "steps": actions,
        "execution_logs": {
            "stdout": execution["stdout"],
            "stderr": execution["stderr"]
        }
    }

    return report
