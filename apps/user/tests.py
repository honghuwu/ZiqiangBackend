"""
Comprehensive unit tests for user app.
Tests cover registration, login, password change, email change, and profile update.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.core import mail
from rest_framework.test import APIClient
from rest_framework import status
from datetime import timedelta
import json

from .models import UserProfile, EmailVerificationCode

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            name='Test User',
            student_id='2023001',
            class_name='Class A',
            phone='12345678901',
            wechat_id='test_wechat'
        )

    def test_user_profile_creation(self):
        """测试用户资料创建"""
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.name, 'Test User')
        self.assertEqual(self.profile.student_id, '2023001')

    def test_user_profile_str_method(self):
        """测试用户资料字符串表示"""
        self.assertEqual(str(self.profile), 'Test User (2023001) - 学生')

    def test_user_role_helper_methods(self):
        """测试角色判断方法"""
        self.assertTrue(self.profile.is_student())
        self.assertFalse(self.profile.is_teacher())
        self.assertFalse(self.profile.is_admin())
        
        # 改为教师
        self.profile.role = 'teacher'
        self.assertFalse(self.profile.is_student())
        self.assertTrue(self.profile.is_teacher())
        self.assertFalse(self.profile.is_admin())

        # 改为管理员
        self.profile.role = 'admin'
        self.assertFalse(self.profile.is_student())
        self.assertFalse(self.profile.is_teacher())
        self.assertTrue(self.profile.is_admin())


class EmailVerificationCodeModelTest(TestCase):
    def setUp(self):
        self.verification_code = EmailVerificationCode.objects.create(
            email='test@example.com',
            code='123456',
            purpose='register'
        )

    def test_verification_code_creation(self):
        """测试验证码创建"""
        self.assertEqual(self.verification_code.email, 'test@example.com')
        self.assertEqual(self.verification_code.code, '123456')
        self.assertEqual(self.verification_code.purpose, 'register')
        self.assertFalse(self.verification_code.is_used)

    def test_delete_expired_codes(self):
        """测试删除过期验证码"""
        # 创建一个过期的验证码
        expired_code = EmailVerificationCode.objects.create(
            email='expired@example.com',
            code='654321',
            purpose='register'
        )
        # 手动将创建时间改为7分钟前
        expired_code.created_at = timezone.now() - timedelta(minutes=7)
        expired_code.save()
        
        # 删除过期验证码(保留6分钟内的)
        deleted_count = EmailVerificationCode.delete_expired(minutes=6)
        
        self.assertEqual(deleted_count, 1)
        self.assertFalse(
            EmailVerificationCode.objects.filter(email='expired@example.com').exists()
        )


class UserAuthViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_data)
        UserProfile.objects.create(
            user=self.user,
            name='Test User',
            student_id='2023001'
        )

    def test_login_success(self):
        """测试成功登录"""
        response = self.client.post(
            '/api/user/login/',
            {
                'student_id': 'testuser',
                'password': 'testpass123'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Login successful')

    def test_get_csrf_token(self):
        """测试获取 CSRF token 接口"""
        response = self.client.get('/api/user/csrf/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('csrfToken', response.data)
        self.assertTrue(response.data['csrfToken'])

    def test_login_failure(self):
        """测试登录失败"""
        response = self.client.post(
            '/api/user/login/',
            {
                'student_id': 'testuser',
                'password': 'wrongpass'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_register_code(self):
        """测试发送注册验证码"""
        response = self.client.post(
            '/api/user/send-register-code/',
            {'email': 'newuser@example.com'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Registration Verification Code', mail.outbox[0].subject)

    def test_send_register_code_invalid_email(self):
        """测试发送注册验证码时使用无效邮箱"""
        response = self.client.post(
            '/api/user/send-register-code/',
            {'email': 'invalid-email'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user(self):
        """测试用户注册"""
        # 先发送验证码
        self.client.post(
            '/api/user/send-register-code/',
            {'email': 'register@example.com'},
            format='json'
        )
        code_obj = EmailVerificationCode.objects.filter(email='register@example.com').first()
        
        # 使用验证码注册
        response = self.client.post(
            '/api/user/register/',
            {
                'student_id': '2023002',
                'name': 'New User',
                'email': 'register@example.com',
                'password': 'newpass123',
                'password_confirm': 'newpass123',
                'code': code_obj.code,
                'phone': '12345678901'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='register@example.com').exists())

    def test_change_password(self):
        """测试修改密码"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/api/user/change-password/',
            {
                'old_password': 'testpass123',
                'new_password': 'newpass456',
                'new_password_confirm': 'newpass456'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 验证密码确实更改了
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass456'))

    def test_send_change_email_code(self):
        """测试发送修改邮箱验证码"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/api/user/send-change-email-code/',
            {'email': 'newemail@example.com'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Email Change Verification Code', mail.outbox[0].subject)

    def test_change_email(self):
        """测试修改邮箱"""
        self.client.force_authenticate(user=self.user)
        
        # 先发送验证码
        self.client.post(
            '/api/user/send-change-email-code/',
            {'email': 'new@example.com'},
            format='json'
        )
        code_obj = EmailVerificationCode.objects.filter(email='new@example.com').first()
        
        # 使用验证码修改邮箱
        response = self.client.post(
            '/api/user/change-email/',
            {
                'email': 'new@example.com',
                'code': code_obj.code
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 验证邮箱确实更改了
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'new@example.com')


class UserRoleTestCase(TestCase):
    """Test user role (teacher/student) functionality"""

    def setUp(self):
        self.client = APIClient()
        self.send_code_url = '/api/user/send-register-code/'
        self.register_url = '/api/user/register/'

    def test_register_as_student_default(self):
        """Test registering as student (default role)"""
        email = 'student@example.com'
        
        # Send verification code
        self.client.post(
            self.send_code_url,
            {'email': email},
            format='json'
        )
        code = EmailVerificationCode.objects.get(email=email).code

        # Register without specifying role (should default to 'student')
        response = self.client.post(
            self.register_url,
            {
                'student_id': '2023001',
                'name': 'Student User',
                'email': email,
                'password': 'password123',
                'password_confirm': 'password123',
                'code': code,
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify role is student
        user = User.objects.get(username='2023001')
        self.assertEqual(user.profile.role, 'student')
        self.assertTrue(user.profile.is_student())
        self.assertFalse(user.profile.is_teacher())

    def test_register_as_teacher(self):
        """Test registering as teacher"""
        email = 'teacher@example.com'
        
        # Send verification code
        self.client.post(
            self.send_code_url,
            {'email': email},
            format='json'
        )
        code = EmailVerificationCode.objects.get(email=email).code

        # Register with role='teacher'
        response = self.client.post(
            self.register_url,
            {
                'student_id': 'T001',
                'name': 'Teacher User',
                'email': email,
                'password': 'password123',
                'password_confirm': 'password123',
                'code': code,
                'role': 'teacher',
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify role is teacher
        user = User.objects.get(username='T001')
        self.assertEqual(user.profile.role, 'teacher')
        self.assertTrue(user.profile.is_teacher())
        self.assertFalse(user.profile.is_student())

    def test_profile_includes_role(self):
        """Test that profile endpoint returns role and email fields"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        profile = UserProfile.objects.create(
            user=user,
            name='Test User',
            student_id='2023001',
            role='student'
        )

        # Login
        self.client.post(
            '/api/user/login/',
            {
                'student_id': 'testuser',
                'password': 'password123'
            },
            format='json'
        )

        # Get profile
        response = self.client.get('/api/user/me/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], 'student')
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_role_is_read_only(self):
        """Test that role field cannot be modified after registration"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        profile = UserProfile.objects.create(
            user=user,
            name='Test User',
            student_id='2023001',
            role='student'
        )

        self.client.force_authenticate(user=user)

        # Try to change role
        response = self.client.patch(
            '/api/user/me/profile/',
            {'role': 'teacher'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify role was not changed (it's read-only)
        profile.refresh_from_db()
        self.assertEqual(profile.role, 'student')

    def test_email_is_read_only_in_profile(self):
        """Test that email cannot be modified through profile endpoint"""
        user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='password123'
        )
        UserProfile.objects.create(
            user=user,
            name='Test User 2',
            student_id='2023002',
            role='student'
        )

        self.client.post(
            '/api/user/login/',
            {
                'student_id': 'testuser2',
                'password': 'password123'
            },
            format='json'
        )

        response = self.client.patch(
            '/api/user/me/profile/',
            {'email': 'hacked@example.com'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertEqual(user.email, 'test2@example.com')

    def test_profile_can_return_admin_role(self):
        """Test that profile endpoint can expose admin role"""
        user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='password123'
        )
        UserProfile.objects.create(
            user=user,
            name='Admin User',
            student_id='A001',
            role='admin'
        )

        self.client.post(
            '/api/user/login/',
            {
                'student_id': 'adminuser',
                'password': 'password123'
            },
            format='json'
        )

        response = self.client.get('/api/user/me/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], 'admin')


class LoginThrottleTestCase(TestCase):
    """Test login rate throttling to prevent brute force"""

    def setUp(self):
        self.login_url = '/api/user/login/'
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        UserProfile.objects.create(
            user=self.user,
            name='Test User',
            student_id='testuser',
        )

    def test_login_throttle_limit(self):
        """Test that login is throttled after 5 attempts per minute"""
        # Use a dedicated client for throttle testing with a unique IP
        client = APIClient()
        client.enforce_csrf_checks = False
        
        # Simulate different IP by setting REMOTE_ADDR header
        # Make 5 failed login attempts
        for i in range(5):
            response = client.post(
                self.login_url,
                {
                    'student_id': 'testuser',
                    'password': 'wrongpassword'
                },
                format='json',
                REMOTE_ADDR='192.168.1.100'
            )
            # All should return 400 (bad request, not throttled)
            self.assertEqual(
                response.status_code, 
                status.HTTP_400_BAD_REQUEST,
                f"Expected 400 on attempt {i+1}, got {response.status_code}"
            )

        # 6th attempt should be throttled
        response = client.post(
            self.login_url,
            {
                'student_id': 'testuser',
                'password': 'wrongpassword'
            },
            format='json',
            REMOTE_ADDR='192.168.1.100'
        )
        # Should return 429 (throttled)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
