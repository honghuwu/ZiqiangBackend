from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("event", "0003_event_status_closed"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventApplication",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("statement", models.TextField(blank=True, default="", verbose_name="申请说明")),
                (
                    "resume",
                    models.FileField(blank=True, null=True, upload_to="applications/resumes/", verbose_name="简历"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "待审核"),
                            ("approved", "已通过"),
                            ("rejected", "已拒绝"),
                            ("cancelled", "已撤回"),
                        ],
                        default="pending",
                        max_length=20,
                        verbose_name="申请状态",
                    ),
                ),
                ("review_note", models.TextField(blank=True, default="", verbose_name="审核备注")),
                ("reviewed_at", models.DateTimeField(blank=True, null=True, verbose_name="审核时间")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="申请时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="applications",
                        to="event.event",
                        verbose_name="项目",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="event_applications",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="申请学生",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
