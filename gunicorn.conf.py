# Gunicorn configuration for Azure App Service
import multiprocessing
import os

# Bind to the port provided by Azure (default 8000)
port = os.getenv("PORT", "8000")
bind = f"0.0.0.0:{port}"

# Worker configuration
# Using 1 worker to fix token sharing issue with in-memory ACTIVE_TOKENS
# For production, consider using Redis for token storage
workers = 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
