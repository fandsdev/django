from app.conf.environ import env
from app.conf.timezone import TIME_ZONE

CELERY_BROKER_URL = env("CELERY_BROKER_URL", cast=str, default="redis://localhost:6379/0")
CELERY_TASK_ALWAYS_EAGER = env("CELERY_TASK_ALWAYS_EAGER", cast=bool, default=env("DEBUG"))
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = False
CELERY_TASK_ACKS_LATE = True
