# Generated by Django 5.0.7 on 2024-08-10 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mybank', '0003_account_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='interest_rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('closed', 'Closed')], default='active', max_length=10),
        ),
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.CharField(choices=[('savings', 'Savings'), ('checking', 'Checking')], max_length=20),
        ),
    ]
