from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("file", "0001_initial"),
        ("event", "0004_eventapplication"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="attachment",
        ),
        migrations.AddField(
            model_name="event",
            name="attachment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="events_as_attachment",
                to="file.managedfile",
                verbose_name="附件",
            ),
        ),
        migrations.RemoveField(
            model_name="eventapplication",
            name="resume",
        ),
        migrations.AddField(
            model_name="eventapplication",
            name="resume",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="applications_as_resume",
                to="file.managedfile",
                verbose_name="简历",
            ),
        ),
    ]
