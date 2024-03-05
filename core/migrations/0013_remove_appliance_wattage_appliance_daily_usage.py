# Generated by Django 5.0.2 on 2024-03-02 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_usage_month_remove_usage_year_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appliance',
            name='wattage',
        ),
        migrations.AddField(
            model_name='appliance',
            name='daily_usage',
            field=models.FloatField(default=0.0),
        ),
    ]