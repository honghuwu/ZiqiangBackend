from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0005_alter_userprofile_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="avatar",
            field=models.ImageField(
                blank=True, upload_to="apps.user.models.avatar_upload_to", verbose_name="头像"
            ),
        ),
    ]
