from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=100, verbose_name="项目名称")),
                ("event_type", models.CharField(max_length=50, verbose_name="项目类型")),
                ("start_time", models.DateTimeField(verbose_name="开始时间")),
                ("end_time", models.DateTimeField(verbose_name="结束时间")),
                ("location", models.CharField(max_length=200, verbose_name="地点")),
                ("cover_image_url", models.URLField(blank=True, verbose_name="封面图片")),
                ("description", models.TextField(verbose_name="项目简介")),
                (
                    "attachment",
                    models.FileField(blank=True, null=True, upload_to="events/attachments/", verbose_name="附件"),
                ),
                ("expected_participants", models.PositiveIntegerField(verbose_name="期望人数")),
                ("current_participants", models.PositiveIntegerField(default=0, verbose_name="当前参与人数")),
                (
                    "status",
                    models.CharField(
                        choices=[("draft", "草稿"), ("published", "已发布"), ("closed", "已关闭")],
                        default="draft",
                        max_length=20,
                        verbose_name="项目状态",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_events",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="发布教师",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
