from django.db import migrations, models


def migrate_removed_to_closed(apps, schema_editor):
    Event = apps.get_model("event", "Event")
    Event.objects.filter(status="removed").update(status="closed")


class Migration(migrations.Migration):

    dependencies = [
        ("event", "0002_remove_event_cover_image_url_and_more"),
    ]

    operations = [
        migrations.RunPython(migrate_removed_to_closed, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="event",
            name="status",
            field=models.CharField(
                choices=[("draft", "草稿"), ("published", "已发布"), ("closed", "已关闭")],
                default="draft",
                max_length=20,
                verbose_name="项目状态",
            ),
        ),
    ]
