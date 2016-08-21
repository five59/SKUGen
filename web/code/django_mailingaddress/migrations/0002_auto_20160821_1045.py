# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-21 14:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_mailingaddress', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingaddress',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_mailingaddress.ISOCountry'),
        ),
    ]