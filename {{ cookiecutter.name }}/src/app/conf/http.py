from app.conf.environ import env


ALLOWED_HOSTS = ["*"]  # Wildcard disables Host header validation, so pls do NOT rely on the Host header in your code with this setting enabled.
CSRF_TRUSTED_ORIGINS = [
    "http://your.app.origin",
]

if env("DEBUG"):
    ABSOLUTE_HOST = "http://localhost:3000"
else:
    ABSOLUTE_HOST = "https://your.app.com"
