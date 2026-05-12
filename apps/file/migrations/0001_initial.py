import uuid

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

import apps.file.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ManagedFile",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("file", models.FileField(upload_to=apps.file.models.managed_file_upload_to, verbose_name="文件")),
                ("original_name", models.CharField(max_length=255, verbose_name="原始文件名")),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("event_attachment", "项目附件"),
                            ("application_resume", "申请简历"),
                            ("template", "系统模板"),
                            ("other", "其他文件"),
                        ],
                        max_length=30,
                        verbose_name="文件分类",
                    ),
                ),
                ("content_type", models.CharField(blank=True, default="", max_length=100, verbose_name="文件类型")),
                ("file_size", models.PositiveBigIntegerField(default=0, verbose_name="文件大小")),
                ("description", models.CharField(blank=True, default="", max_length=255, verbose_name="文件说明")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                (
                    "uploaded_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="managed_files",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="上传者",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="FileTemplate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.SlugField(max_length=50, unique=True, verbose_name="模板键")),
                ("name", models.CharField(max_length=100, verbose_name="模板名称")),
                ("description", models.TextField(blank=True, default="", verbose_name="模板说明")),
                ("is_active", models.BooleanField(default=True, verbose_name="是否启用")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                (
                    "file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="template_bindings",
                        to="file.managedfile",
                        verbose_name="模板文件",
                    ),
                ),
            ],
            options={"ordering": ["key"]},
        ),
    ]
