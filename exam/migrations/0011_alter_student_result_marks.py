# Generated by Django 4.0.1 on 2022-01-11 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0010_student_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_result',
            name='marks',
            field=models.PositiveBigIntegerField(blank=True, default=0, null=True),
        ),
    ]
