# Generated by Django 3.2.18 on 2023-04-25 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_action_manager', '0002_salesledgertransactionsmodels'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SalesLedgerTransactionsModels',
        ),
        migrations.AddField(
            model_name='user',
            name='user_email',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
