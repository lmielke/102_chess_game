# Generated by Django 2.1.1 on 2018-11-12 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_article_web_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='web_mode',
            field=models.CharField(default=0, max_length=3),
            preserve_default=False,
        ),
    ]
