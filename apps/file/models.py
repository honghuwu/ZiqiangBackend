import os
import uuid

from django.conf import settings
from django.db import models


def managed_file_upload_to(instance, filename):
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    return f"managed-files/{instance.category}/{instance.id}{ext}"


class ManagedFile(models.Model):
    CATEGORY_EVENT_ATTACHMENT = "event_attachment"
    CATEGORY_APPLICATION_RESUME = "application_resume"
    CATEGORY_TEMPLATE = "template"
    CATEGORY_OTHER = "other"

    CATEGORY_CHOICES = (
        (CATEGORY_EVENT_ATTACHMENT, "项目附件"),
        (CATEGORY_APPLICATION_RESUME, "申请简历"),
        (CATEGORY_TEMPLATE, "系统模板"),
        (CATEGORY_OTHER, "其他文件"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField("文件", upload_to=managed_file_upload_to)
    original_name = models.CharField("原始文件名", max_length=255)
    category = models.CharField("文件分类", max_length=30, choices=CATEGORY_CHOICES)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_files",
        verbose_name="上传者",
    )
    content_type = models.CharField("文件类型", max_length=100, blank=True, default="")
    file_size = models.PositiveBigIntegerField("文件大小", default=0)
    description = models.CharField("文件说明", max_length=255, blank=True, default="")
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.original_name} ({self.category})"

    def is_referenced(self):
        return any(
            (
                self.template_bindings.exists(),
                self.events_as_attachment.exists(),
                self.applications_as_resume.exists(),
            )
        )

    def can_delete(self):
        return not self.is_referenced()


class FileTemplate(models.Model):
    key = models.SlugField("模板键", max_length=50, unique=True)
    name = models.CharField("模板名称", max_length=100)
    description = models.TextField("模板说明", blank=True, default="")
    file = models.ForeignKey(
        ManagedFile,
        on_delete=models.PROTECT,
        related_name="template_bindings",
        verbose_name="模板文件",
    )
    is_active = models.BooleanField("是否启用", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        ordering = ["key"]

    def __str__(self):
        return f"{self.key}: {self.name}"


class FileAuditLog(models.Model):
    ACTION_UPLOAD = "upload"
    ACTION_DOWNLOAD = "download"
    ACTION_DELETE = "delete"
    ACTION_DELETE_BLOCKED = "delete_blocked"
    ACTION_TEMPLATE_CREATE = "template_create"
    ACTION_TEMPLATE_UPDATE = "template_update"
    ACTION_TEMPLATE_DISABLE = "template_disable"

    ACTION_CHOICES = (
        (ACTION_UPLOAD, "上传文件"),
        (ACTION_DOWNLOAD, "下载文件"),
        (ACTION_DELETE, "删除文件"),
        (ACTION_DELETE_BLOCKED, "删除被阻止"),
        (ACTION_TEMPLATE_CREATE, "创建模板"),
        (ACTION_TEMPLATE_UPDATE, "更新模板"),
        (ACTION_TEMPLATE_DISABLE, "停用模板"),
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="file_audit_logs",
        verbose_name="操作人",
    )
    action = models.CharField("操作类型", max_length=30, choices=ACTION_CHOICES)
    managed_file = models.ForeignKey(
        ManagedFile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
        verbose_name="关联文件",
    )
    template_key = models.SlugField("模板键", max_length=50, blank=True, default="")
    ip_address = models.CharField("IP 地址", max_length=64, blank=True, default="")
    user_agent = models.TextField("User-Agent", blank=True, default="")
    metadata = models.JSONField("附加数据", blank=True, default=dict)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} by {self.actor_id or 'anonymous'}"
