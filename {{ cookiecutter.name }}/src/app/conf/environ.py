import environ  # type: ignore[import-untyped]

from app.conf.boilerplate import BASE_DIR


env = environ.Env(
    DEBUG=(bool, False),
    CI=(bool, False),
)

envpath = BASE_DIR / ".env"

if envpath.exists():
    env.read_env(envpath)

__all__ = [
    "env",
]
