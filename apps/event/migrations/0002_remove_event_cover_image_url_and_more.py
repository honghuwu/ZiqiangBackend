from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("event", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="cover_image_url",
        ),
        migrations.AlterField(
            model_name="event",
            name="end_time",
            field=models.DateTimeField(blank=True, null=True, verbose_name="结束时间"),
        ),
        migrations.AlterField(
            model_name="event",
            name="location",
            field=models.CharField(blank=True, default="", max_length=200, verbose_name="地点"),
        ),
    ]
