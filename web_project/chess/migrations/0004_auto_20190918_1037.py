# Generated by Django 2.2.5 on 2019-09-18 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess', '0003_auto_20190914_1343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chess',
            old_name='activeBoard',
            new_name='boardText',
        ),
        migrations.AlterField(
            model_name='chess',
            name='gameImage',
            field=models.ImageField(default='chessboard_oFsGPaG_VTJL2pL.jpg', upload_to='chess_pics', verbose_name='Formate: jpg, gif, bmp'),
        ),
    ]
