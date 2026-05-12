from django.conf import settings
from django.db import models
from django.utils import timezone


class Notification(models.Model):
    TYPE_EVENT_APPLICATION_SUBMITTED = "event_application_submitted"
    TYPE_EVENT_APPLICATION_APPROVED = "event_application_approved"
    TYPE_EVENT_APPLICATION_REJECTED = "event_application_rejected"

    TYPE_CHOICES = (
        (TYPE_EVENT_APPLICATION_SUBMITTED, "项目申请提交"),
        (TYPE_EVENT_APPLICATION_APPROVED, "项目申请通过"),
        (TYPE_EVENT_APPLICATION_REJECTED, "项目申请拒绝"),
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="接收人",
    )
    notification_type = models.CharField("通知类型", max_length=50, choices=TYPE_CHOICES)
    title = models.CharField("标题", max_length=200)
    content = models.TextField("内容")
    is_read = models.BooleanField("是否已读", default=False)
    read_at = models.DateTimeField("已读时间", blank=True, null=True)
    metadata = models.JSONField("附加数据", blank=True, default=dict)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.recipient_id}: {self.title}"

    def mark_as_read(self):
        if self.is_read:
            return
        self.is_read = True
        self.read_at = timezone.now()
        self.save(update_fields=["is_read", "read_at", "updated_at"])
