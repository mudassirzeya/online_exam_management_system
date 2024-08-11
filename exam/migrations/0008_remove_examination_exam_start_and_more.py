# Generated by Django 4.0.1 on 2022-01-10 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0007_response_table_exam_associated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examination',
            name='exam_start',
        ),
        migrations.AddField(
            model_name='examination',
            name='exam_end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='examination',
            name='exam_start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
