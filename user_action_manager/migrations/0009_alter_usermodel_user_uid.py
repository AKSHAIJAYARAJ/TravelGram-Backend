# Generated by Django 3.2.18 on 2023-06-11 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_action_manager', '0008_alter_usermodel_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='user_uid',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
