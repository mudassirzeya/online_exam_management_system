# Generated by Django 4.0.1 on 2022-01-06 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile_company_assign_and_more'),
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=100, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.adminuser')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(blank=True, null=True)),
                ('question_image', models.TextField(blank=True, null=True)),
                ('option_a', models.TextField(blank=True, null=True)),
                ('option_a_image', models.TextField(blank=True, null=True)),
                ('option_b', models.TextField(blank=True, null=True)),
                ('option_b_image', models.TextField(blank=True, null=True)),
                ('option_c', models.TextField(blank=True, null=True)),
                ('option_c_image', models.TextField(blank=True, null=True)),
                ('option_d', models.TextField(blank=True, null=True)),
                ('option_d_image', models.TextField(blank=True, null=True)),
                ('marks', models.IntegerField(blank=True, null=True)),
                ('associated_exam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.examination')),
                ('section_dropdown', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.section')),
            ],
        ),
    ]
