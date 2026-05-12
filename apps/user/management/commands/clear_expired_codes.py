from django.core.management.base import BaseCommand
from apps.user.models import EmailVerificationCode

class Command(BaseCommand):
    help = '清除过期的邮箱验证码'

    def add_arguments(self, parser):
        parser.add_argument(
            '--minutes',
            type=int,
            default=5,
            help='保留验证码的分钟数，默认为5分钟'
        )

    def handle(self, *args, **options):
        minutes = options['minutes']
        deleted_count = EmailVerificationCode.delete_expired(minutes)
        self.stdout.write(
            self.style.SUCCESS(
                f'成功清除 {deleted_count} 条过期验证码记录'
            )
        )