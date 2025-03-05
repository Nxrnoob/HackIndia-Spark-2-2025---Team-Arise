import subprocess
import time

# Start Flask API (Backend)
backend_process = subprocess.Popen(["python", "backend.py"])

# Wait for API to start (optional delay)
time.sleep(3)  

# Start Streamlit UI (Frontend)
frontend_process = subprocess.Popen(["streamlit", "run", "frontend.py"])

# Keep both running
backend_process.wait()
frontend_process.wait()

