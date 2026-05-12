from .models import Notification


def create_notification(*, recipient, notification_type, title, content, metadata=None):
    return Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        content=content,
        metadata=metadata or {},
    )


def notify_event_application_submitted(*, teacher, student, event, application):
    create_notification(
        recipient=teacher,
        notification_type=Notification.TYPE_EVENT_APPLICATION_SUBMITTED,
        title=f"收到新的项目申请：{event.title}",
        content=f"{getattr(student.profile, 'name', student.username)} 提交了项目申请，请尽快审核。",
        metadata={
            "event_id": event.id,
            "application_id": application.id,
            "student_id": student.id,
        },
    )


def notify_event_application_reviewed(*, student, event, application, approved):
    notification_type = (
        Notification.TYPE_EVENT_APPLICATION_APPROVED
        if approved
        else Notification.TYPE_EVENT_APPLICATION_REJECTED
    )
    title = f"你的项目申请已{'通过' if approved else '被拒绝'}：{event.title}"
    content = "请查看项目详情和后续安排。" if approved else "请查看老师的审核备注。"
    create_notification(
        recipient=student,
        notification_type=notification_type,
        title=title,
        content=content,
        metadata={
            "event_id": event.id,
            "application_id": application.id,
            "approved": approved,
        },
    )
