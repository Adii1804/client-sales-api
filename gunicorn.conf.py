# Gunicorn configuration for Azure App Service
import multiprocessing
import os

# Bind to the port provided by Azure (default 8000)
port = os.getenv("PORT", "8000")
bind = f"0.0.0.0:{port}"

# Worker configuration
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
