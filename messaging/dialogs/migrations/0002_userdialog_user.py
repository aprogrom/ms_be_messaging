# Generated by Django 3.1.4 on 2020-12-16 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('relations', '0001_initial'),
        ('dialogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdialog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dialogs', to='relations.userrelationmodel'),
        ),
    ]
