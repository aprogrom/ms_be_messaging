# Generated by Django 3.1.4 on 2020-12-29 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relations', '0001_initial'),
        ('messages', '0002_auto_20201216_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to='relations.userrelationmodel'),
        ),
    ]