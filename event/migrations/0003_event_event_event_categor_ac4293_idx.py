# Generated by Django 5.1 on 2024-08-31 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_alter_category_options_alter_event_options_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='event',
            index=models.Index(fields=['category', 'priority'], name='event_event_categor_ac4293_idx'),
        ),
    ]
