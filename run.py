import subprocess
import time
import sys
import os

def run_app():
    print(" Starting AI QA System...")
    print("--------------------------------")

    
    print("🔹 Launching Backend (app.server)...")
    backend = subprocess.Popen(
        [sys.executable, "-m", "app.server"],
        cwd=os.getcwd(),
        env=os.environ.copy()
        
    )

   

def run_app():
    print("🚀 STARTING AI SYSTEM")
    
    # 1. Start Backend
    print("🔹 Launching Backend...")
    backend = subprocess.Popen([sys.executable, "-m", "app.server"], cwd=os.getcwd())
    
    # 2. Wait for API
    print("🔹 Waiting for API...")
    for i in range(10):
        try:
            requests.get("http://127.0.0.1:5000")
            print(" API Online!")
            break
        except:
            time.sleep(1)
            
    # 3. Start Frontend
    print("🔹 Launching UI...")
    frontend = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], cwd=os.getcwd())
    
    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        backend.terminate()
        frontend.terminate()

if __name__ == "__main__":
    run_app()
    print(" Waiting 5 seconds for Backend to startup...")
    time.sleep(5) 

    
    if backend.poll() is not None:
        print("\n CRITICAL ERROR: The Backend Server crashed immediately!")
        print("   Please run 'python -m app.server' manually to see the error.")
        sys.exit(1)

    print(" Backend seems alive!")

    
    print("🔹 Launching Frontend (streamlit_app.py)...")
    frontend = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app.py"],
        cwd=os.getcwd(),
        env=os.environ.copy()
    )

    print("\n🎉 System is Running!")
    print("   -> Backend: http://127.0.0.1:5000")
    print("   -> Frontend: http://localhost:8501")
    print("   (Press Ctrl+C to stop)")

    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("\n Shutting down...")
        backend.terminate()
        frontend.terminate()

if __name__ == "__main__":
    run_app()