# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-30 02:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('brief', models.CharField(blank=True, max_length=255, null=True)),
                ('content', models.TextField(verbose_name='文章内容')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('head_img', models.ImageField(blank=True, null=True, upload_to='uploads', verbose_name='文章标题图片')),
                ('status', models.CharField(choices=[('draft', '草稿'), ('published', '已发布'), ('hidden', '隐藏')], default='published', max_length=32)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('signature', models.CharField(blank=True, max_length=255, null=True)),
                ('head_img', models.ImageField(blank=True, height_field=150, null=True, upload_to='', width_field=150)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
