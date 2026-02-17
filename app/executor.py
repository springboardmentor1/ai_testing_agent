import subprocess

def run_test():
    try:
        subprocess.run(["python", "generated_test.py"], check=True)
        return "PASS"
    except:
        return "FAIL"