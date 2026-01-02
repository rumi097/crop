import os

# Railway (and most PaaS) provide the listening port via PORT.
# Use a safe default for local/docker runs.
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"

# Keep defaults conservative; allow override via env.
workers = int(os.getenv('WEB_CONCURRENCY', '1'))
threads = int(os.getenv('GUNICORN_THREADS', '1'))
timeout = int(os.getenv('GUNICORN_TIMEOUT', '120'))
