# Generated by Django 4.0.1 on 2022-01-06 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_section_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='section',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='add_student_link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(blank=True, max_length=100, null=True)),
                ('exam_associated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.examination')),
            ],
        ),
        migrations.CreateModel(
            name='add_question_link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(blank=True, max_length=100, null=True)),
                ('exam_associated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.examination')),
            ],
        ),
    ]
