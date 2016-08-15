# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-14 20:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20160814_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='code',
            field=models.CharField(default='', help_text='Three-Character', max_length=3, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='code',
            field=models.CharField(default='', help_text='Two-Characters', max_length=2, verbose_name='Code'),
        ),
    ]