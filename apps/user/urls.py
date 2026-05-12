from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
    AvatarUploadView,
    SendRegisterCodeView,
    RegisterView,
    LoginView,
    LogoutView,
    CsrfTokenView,
    MeProfileView,
    ChangePasswordView,
    SendChangeEmailCodeView,
    ChangeEmailView,
)

urlpatterns = [
    path('send-register-code/', SendRegisterCodeView.as_view(), name='send-register-code'),
    path('register/', RegisterView.as_view(), name='register'),
    
    path('login/', csrf_exempt(LoginView.as_view()), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('csrf/', CsrfTokenView.as_view(), name='csrf-token'),
    
    path('me/profile/', MeProfileView.as_view(), name='me-profile'),
    path('me/avatar/', AvatarUploadView.as_view(), name='me-avatar'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    path('send-change-email-code/', SendChangeEmailCodeView.as_view(), name='send-change-email-code'),
    path('change-email/', ChangeEmailView.as_view(), name='change-email'),
]

