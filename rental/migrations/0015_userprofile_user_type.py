# Generated by Django 3.0.6 on 2020-06-18 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0014_auto_20200617_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('FR', 'FREE'), ('BS', 'BASIC'), ('PR', 'PREMIUM')], default='FR', max_length=2),
        ),
    ]
