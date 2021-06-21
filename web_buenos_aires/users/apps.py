from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "web_buenos_aires.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import web_buenos_aires.users.signals  # noqa F401
        except ImportError:
            pass
