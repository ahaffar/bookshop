# Generated by Django 3.0.6 on 2020-06-19 17:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0020_auto_20200619_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowed',
            name='due_back',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 20, 17, 1, 26, 755732)),
        ),
    ]