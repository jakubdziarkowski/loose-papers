import os

# ----------------------------------------
# Database
# ----------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "loose_papers"),
        "USER": os.getenv("POSTGRES_USER", "loose"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "loose"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": 5432,
    }
}

# ----------------------------------------
# Redis / RQ
# ----------------------------------------
RQ_QUEUES = {
    "default": {
        "HOST": os.getenv("REDIS_HOST", "localhost"),
        "PORT": 6379,
        "DB": 0,
    }
}
