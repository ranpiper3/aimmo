# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-07-23 14:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('aimmo', '0017_remove_game_game_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games_for_class', to='common.Class'),
        ),
    ]
