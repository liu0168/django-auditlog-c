from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class AuditlogConfig(AppConfig):
    name = "auditlog"
    verbose_name = _("Audit log")
    default_auto_field = "django.db.models.AutoField"
    label = "auditlog"

    def ready(self):
        from auditlog.registry import auditlog
        self.label = getattr(settings, 'AUDITLOG_APP_NAME', self.label)

        auditlog.register_from_settings()

        from auditlog import models

        models.changes_func = models._changes_func()
        for model in self.get_models():
            model._meta.app_label = self.label
