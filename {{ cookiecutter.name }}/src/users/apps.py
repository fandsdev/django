from django.utils.translation import gettext_lazy as _

from app.base_config import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    default = True
    name = "users"
    verbose_name = _("Users")
