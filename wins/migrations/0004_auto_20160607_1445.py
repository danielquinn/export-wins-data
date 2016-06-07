# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-07 14:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wins', '0003_auto_20160531_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='win',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='wins.Win'),
        ),
    ]
