from app.conf.environ import env

DEFAULT_FILE_STORAGE = env('DEFAULT_FILE_STORAGE', cast=str, default='django.core.files.storage.FileSystemStorage')
