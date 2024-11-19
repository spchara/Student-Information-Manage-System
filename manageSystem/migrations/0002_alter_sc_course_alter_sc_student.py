# Generated by Django 5.1.3 on 2024-11-17 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageSystem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sc',
            name='course',
            field=models.ForeignKey(default='DEFAULT_COURSE_ID', on_delete=django.db.models.deletion.CASCADE, to='manageSystem.course'),
        ),
        migrations.AlterField(
            model_name='sc',
            name='student',
            field=models.ForeignKey(default='DEFAULT_STUDENT_ID', on_delete=django.db.models.deletion.CASCADE, to='manageSystem.student'),
        ),
    ]