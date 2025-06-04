import environ  # type: ignore[import-untyped]

from app.conf.boilerplate import SRC_DIR


env = environ.Env(
    DEBUG=(bool, False),
    CI=(bool, False),
)

envpath = SRC_DIR / "app" / ".env"

if envpath.exists():
    env.read_env(envpath)

__all__ = [
    "env",
]
