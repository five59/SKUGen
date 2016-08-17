# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-17 08:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20160817_0425'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='asin_id',
            field=models.CharField(blank=True, default='', help_text='Amazon Standard ID Number', max_length=10, verbose_name='ASIN'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='dimension_depth',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, help_text='In Inches', max_digits=10, verbose_name='Product Depth'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='dimension_height',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, help_text='In Inches', max_digits=10, verbose_name='Product Height'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='dimension_width',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, help_text='In Inches', max_digits=10, verbose_name='Product Width'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='weight_product',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, help_text='In Ounces', max_digits=10, verbose_name='Product Weight'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='weight_shipping',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, help_text='In Ounces', max_digits=10, verbose_name='Shipping Weight'),
        ),
    ]
