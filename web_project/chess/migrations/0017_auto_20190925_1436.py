# Generated by Django 2.2.5 on 2019-09-25 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess', '0016_auto_20190925_1031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chess',
            name='playerColor',
        ),
        migrations.AlterField(
            model_name='chess',
            name='removeds',
            field=models.TextField(max_length=1000),
        ),
    ]
