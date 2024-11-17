# Generated by Django 5.1.3 on 2024-11-17 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageSystem', '0003_alter_course_ccredit'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='course',
            name='course_chk_1',
        ),
        migrations.AddConstraint(
            model_name='course',
            constraint=models.CheckConstraint(check=models.Q(Ccredit__range=(0, 10)), name='course_chk_1'),
        ),
    ]
