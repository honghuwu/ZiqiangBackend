from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.user.models import UserProfile

from .models import Notification


class NotificationAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="notifyuser",
            email="notify@example.com",
            password="password123",
        )
        UserProfile.objects.create(
            user=self.user,
            name="Notify User",
            student_id="2023555",
            role=UserProfile.ROLE_STUDENT,
            class_name="Class 1",
        )
        self.notification = Notification.objects.create(
            recipient=self.user,
            notification_type=Notification.TYPE_EVENT_APPLICATION_SUBMITTED,
            title="测试通知",
            content="这是一条测试通知",
        )

    def test_user_can_list_notifications(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/notification/my/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_user_can_mark_notification_read(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f"/api/notification/my/{self.notification.id}/read/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
