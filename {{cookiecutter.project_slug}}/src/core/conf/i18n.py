from pathlib import Path

from core.conf.boilerplate import BASE_DIR

LANGUAGE_CODE = "ru"

LOCALE_PATHS = [Path(BASE_DIR).parent / "locale"]

USE_i18N = True
