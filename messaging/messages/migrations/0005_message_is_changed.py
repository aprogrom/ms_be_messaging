# Generated by Django 3.1.4 on 2020-12-29 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messages', '0004_auto_20201229_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_changed',
            field=models.BooleanField(default=False),
        ),
    ]
