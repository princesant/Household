# URL of the broker for managing task queues
broker_url = "redis://localhost:6379/1"

# URL of the backend for storing task results
result_backend = "redis://localhost:6379/2"

# Set the timezone for the Celery app
timezone = "Asia/Kolkata"

# Ensure broker retries connection on startup failure
broker_connection_retry_on_startup = True
