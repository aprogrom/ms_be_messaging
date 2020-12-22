# Generated by Django 3.1.4 on 2020-12-16 09:30

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mscore', '0009_auto_20200925_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRelationModel',
            fields=[
                ('relationbasemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mscore.relationbasemodel')),
            ],
            options={
                'abstract': False,
                'default_manager_name': 'default_manager',
            },
            bases=('mscore.relationbasemodel',),
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]