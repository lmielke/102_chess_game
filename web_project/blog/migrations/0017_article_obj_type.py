# Generated by Django 2.1.1 on 2019-06-17 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20181221_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='obj_type',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]