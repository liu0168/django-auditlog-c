import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.apps import apps

from ..models import get_log_entry_table_name


def get_app_label():
    return apps.get_containing_app_config('auditlog').label

class Migration(migrations.Migration):

    @property
    def app_label(self):
        return apps.get_containing_app_config('auditlog').label

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contenttypes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LogEntry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("object_pk", models.TextField(verbose_name="object pk")),
                (
                    "object_id",
                    models.PositiveIntegerField(
                        db_index=True, null=True, verbose_name="object id", blank=True
                    ),
                ),
                ("object_repr", models.TextField(verbose_name="object representation")),
                (
                    "action",
                    models.PositiveSmallIntegerField(
                        verbose_name="action",
                        choices=[(0, "create"), (1, "update"), (2, "delete")],
                    ),
                ),
                (
                    "changes",
                    models.TextField(verbose_name="change message", blank=True),
                ),
                (
                    "timestamp",
                    models.DateTimeField(auto_now_add=True, verbose_name="timestamp"),
                ),
                (
                    "actor",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        verbose_name="actor",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        verbose_name="content type",
                        to="contenttypes.ContentType",
                    ),
                ),
            ],
            options={
                'app_label': get_app_label,
                'db_table': get_log_entry_table_name,
                "ordering": ["-timestamp"],
                "get_latest_by": "timestamp",
                "verbose_name": "log entry",
                "verbose_name_plural": "log entries",
            },
            bases=(models.Model,),
        ),
    ]
