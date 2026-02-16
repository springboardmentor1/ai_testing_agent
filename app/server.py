from flask import Flask, request, jsonify, Response, send_from_directory
from app.agents.baseline_agent import agent_app
import datetime
import csv
import io
import os

app = Flask(__name__, static_folder="../static")
TEST_HISTORY = []

@app.route('/')
def home():
    return jsonify({"status": "Online", "message": "Use Streamlit Frontend"})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('../static', filename)

@app.route('/api/run-test', methods=['POST'])
def run_test():
    data = request.json
    instruction = data.get('instruction')
    
    print(f"🔹 Processing: {instruction}")
    
    
    logs = []
    try:
        result = agent_app.invoke({"input": instruction})
        logs = result.get("execution_logs", [])
    except Exception as e:
        print(f"❌ Agent Execution Failed: {e}")
        logs = [{"status": "error", "message": f"Critical Agent Crash: {str(e)}"}]

    
    status = "PASSED"
    clean_steps = []

    if not logs:
        clean_steps.append("No steps executed (Agent returned empty logs).")
        status = "FAILED"
    else:
        for i, log in enumerate(logs):
            
            if isinstance(log, dict):
                msg = log.get('message', 'Unknown Action')
                if log.get('status') == 'error':
                    status = "FAILED"
            else:
                msg = str(log)
                if "error" in msg.lower(): status = "FAILED"
            
            
            step_str = f"{i+1}. {msg}"
            clean_steps.append(step_str)

    # Join steps into a single block of text
    steps_text_block = "\n".join(clean_steps)
    
    
    print("------------------------------------------------")
    print(f"✅ GENERATED STEPS FOR REPORT:\n{steps_text_block}")
    print("------------------------------------------------")

    
    report = {
        "id": len(TEST_HISTORY) + 1,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "instruction": instruction,
        "status": status,
        "logs": logs,
        "steps_text": steps_text_block  
    }
    TEST_HISTORY.insert(0, report)
    
    return jsonify({"status": "success", "report": report})

@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify(TEST_HISTORY)

@app.route('/api/export', methods=['GET'])
def export_report():
    """Generates a CSV file where 'Steps' are correctly formatted."""
    output = io.StringIO()
    
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    
    writer.writerow(['ID', 'Timestamp', 'Test Case Description', 'Status', 'Execution Steps'])
    
    for r in TEST_HISTORY:
        
        steps = r.get('steps_text', 'No steps recorded.')
        
        writer.writerow([
            r['id'], 
            r['timestamp'], 
            r['instruction'], 
            r['status'], 
            steps 
        ])
    
    return Response(
        output.getvalue(), 
        mimetype="text/csv", 
        headers={"Content-disposition": "attachment; filename=test_report.csv"}
    )

if __name__ == '__main__':
    print("⚡ Starting Flask API on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)