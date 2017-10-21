# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-21 08:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Earth', '0004_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='md',
            field=models.TextField(default=django.utils.timezone.now, verbose_name='文章内容'),
            preserve_default=False,
        ),
    ]
