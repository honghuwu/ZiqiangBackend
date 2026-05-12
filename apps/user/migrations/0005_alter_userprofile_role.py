from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0004_userprofile_role_alter_userprofile_class_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="role",
            field=models.CharField(
                choices=[
                    ("student", "学生"),
                    ("teacher", "教师"),
                    ("admin", "管理员"),
                ],
                default="student",
                max_length=10,
                verbose_name="角色",
            ),
        ),
    ]
