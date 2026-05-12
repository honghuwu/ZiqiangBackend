from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer


class MyNotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        queryset = Notification.objects.filter(recipient=self.request.user)
        is_read = self.request.query_params.get("is_read")
        if is_read == "true":
            queryset = queryset.filter(is_read=True)
        elif is_read == "false":
            queryset = queryset.filter(is_read=False)
        return queryset


class MyNotificationDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)


class MarkNotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        notification = Notification.objects.filter(recipient=request.user, pk=pk).first()
        if notification is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        notification.mark_as_read()
        return Response(NotificationSerializer(notification).data, status=status.HTTP_200_OK)


class MarkAllNotificationsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        unread_notifications = Notification.objects.filter(recipient=request.user, is_read=False)
        for notification in unread_notifications:
            notification.mark_as_read()
        return Response({"detail": "All notifications marked as read."}, status=status.HTTP_200_OK)
