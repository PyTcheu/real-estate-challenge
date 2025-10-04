import subprocess
import time
import os

# Run FastAPI with Gunicorn (ASGI) for better performance and scalability
# Using workers for demonstration; adjust based on your CPU cores and load

# You can also get the numbers of CPU cores programmatically if needed

num_workers = os.cpu_count()

api = subprocess.Popen([
    "gunicorn",
    "app.app:app",
    "-k", "uvicorn.workers.UvicornWorker",
    "--bind", "0.0.0.0:8000",
    "--workers", str(num_workers)
])

time.sleep(3)

streamlit = subprocess.Popen([
    "streamlit", "run", "app/main.py",
    "--server.port", "8501",
    "--server.address", "0.0.0.0"
])

# Keep both alive
api.wait()
streamlit.wait()
