# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-05 03:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='手机号码'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(null=True, upload_to='users', verbose_name='头像'),
        ),
    ]
