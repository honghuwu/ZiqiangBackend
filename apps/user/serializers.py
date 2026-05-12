from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
import datetime

from .models import UserProfile, EmailVerificationCode

class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer: student_id and role cannot be modified"""
    email = serializers.EmailField(source='user.email', read_only=True)
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'student_id', 'class_name', 'phone', 'wechat_id', 'bio', 'role', 'email', 'avatar', 'avatar_url']
        read_only_fields = ['id', 'student_id', 'role', 'email', 'avatar_url']

    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None


class SendRegisterCodeSerializer(serializers.Serializer):
    """Send verification code for registration"""
    email = serializers.EmailField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is already registered')
        return value


class RegisterSerializer(serializers.Serializer):
    """User registration serializer"""
    student_id = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    code = serializers.CharField(max_length=6)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    wechat_id = serializers.CharField(max_length=50, required=False, allow_blank=True)
    class_name = serializers.CharField(max_length=50, required=False, allow_blank=True)
    # Admin role should be provisioned by backend/admin, not self-registered.
    role = serializers.ChoiceField(
        choices=[UserProfile.ROLE_STUDENT, UserProfile.ROLE_TEACHER],
        required=False,
        default=UserProfile.ROLE_STUDENT,
    )

    def validate(self, attrs):
        # Check if student_id and email are already registered
        if User.objects.filter(username=attrs['student_id']).exists():
            raise serializers.ValidationError('This student_id is already registered')
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('This email is already registered')

        # Check if passwords match
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('Passwords do not match')

        # Validate email verification code (expires after 5 minutes)
        try:
            record = EmailVerificationCode.objects.filter(
                email=attrs['email'],
                code=attrs['code'],
                purpose='register',
                is_used=False,
            ).latest('created_at')
        except EmailVerificationCode.DoesNotExist:
            raise serializers.ValidationError('Invalid or non-existent verification code')

        if timezone.now() - record.created_at > datetime.timedelta(minutes=5):
            raise serializers.ValidationError('Verification code has expired')

        attrs['code_record'] = record
        return attrs

    def create(self, validated_data):
        code_record = validated_data.pop('code_record')
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')
        email = validated_data.pop('email')
        student_id = validated_data.pop('student_id')
        name = validated_data.pop('name')
        role = validated_data.pop('role', UserProfile.ROLE_STUDENT)

        # 创建用户
        user = User.objects.create_user(
            username=student_id,
            email=email,
            password=password,
        )

        # 创建用户信息
        UserProfile.objects.create(
            user=user,
            name=name,
            student_id=student_id,
            class_name=validated_data.pop('class_name', ''),
            phone=validated_data.pop('phone', ''),
            wechat_id=validated_data.pop('wechat_id', ''),
            role=role,
        )

        # 标记验证码已使用
        code_record.is_used = True
        code_record.save()

        return user


class LoginSerializer(serializers.Serializer):
    """Login serializer: student_id + password"""
    student_id = serializers.CharField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(required=False, default=False)


class ChangePasswordSerializer(serializers.Serializer):
    """Change password serializer"""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)
    new_password_confirm = serializers.CharField(write_only=True, min_length=6)

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError('Old password is incorrect')
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError('New passwords do not match')
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        update_session_auth_hash(self.context['request'], user)
        return user


class SendChangeEmailCodeSerializer(serializers.Serializer):
    """Send verification code for email change"""
    email = serializers.EmailField()

    def validate_email(self, value):
        user = self.context['request'].user
        # New email cannot be used by others
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError('This email is already in use')
        return value


class ChangeEmailSerializer(serializers.Serializer):
    """Change email serializer"""
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        user = self.context['request'].user
        email = attrs['email']
        code = attrs['code']

        # Email cannot be used by others
        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            raise serializers.ValidationError('This email is already in use')

        # Validate email verification code
        try:
            record = EmailVerificationCode.objects.filter(
                email=email,
                code=code,
                purpose='change_email',
                is_used=False,
            ).latest('created_at')
        except EmailVerificationCode.DoesNotExist:
            raise serializers.ValidationError('Invalid or non-existent verification code')

        if timezone.now() - record.created_at > datetime.timedelta(minutes=5):
            raise serializers.ValidationError('Verification code has expired')

        attrs['code_record'] = record
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        code_record = self.validated_data.pop('code_record')
        email = self.validated_data['email']

        user.email = email
        user.save()

        code_record.is_used = True
        code_record.save()

        return user


class AvatarUploadSerializer(serializers.Serializer):
    avatar = serializers.ImageField()
