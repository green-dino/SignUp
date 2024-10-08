# Generated by Django 5.1 on 2024-08-27 18:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['start_date'], 'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Category Name'),
        ),
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='event.category'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(verbose_name='End Date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Event Name'),
        ),
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Organizer'),
        ),
        migrations.AlterField(
            model_name='event',
            name='priority',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=1, verbose_name='Priority'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(verbose_name='Start Date'),
        ),
        migrations.AddIndex(
            model_name='event',
            index=models.Index(fields=['start_date'], name='event_event_start_d_d4a35f_idx'),
        ),
        migrations.AddIndex(
            model_name='event',
            index=models.Index(fields=['end_date'], name='event_event_end_dat_18315b_idx'),
        ),
    ]
