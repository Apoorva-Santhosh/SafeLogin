import os

LOGGING = {
    "version": 1,
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/security.log"),
        },
    },
    "loggers": {
        "security": {
            "handlers": ["file"],
            "level": "WARNING",
        },
    },
}