from app.conf.boilerplate import BASE_DIR
from app.conf.environ import env


MEDIA_URL = "/media/"
MEDIA_ROOT = env.path("MEDIA_ROOT", default=BASE_DIR / "media")
