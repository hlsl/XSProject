# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-05 02:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artapp', '0004_auto_20180704_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='art',
            name='img',
            field=models.ImageField(default='http://www.freexs.org/modules/article/images/nocover.jpg', upload_to='images', verbose_name='文章的图片'),
        ),
    ]
