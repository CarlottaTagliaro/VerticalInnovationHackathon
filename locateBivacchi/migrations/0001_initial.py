# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-16 18:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bivacco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coordinate_x', models.FloatField()),
                ('coordinaye_y', models.FloatField()),
                ('capability', models.IntegerField(default=0)),
                ('height', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('person_number', models.IntegerField(default=0)),
                ('id_bivacco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locateBivacchi.Bivacco')),
            ],
        ),
        migrations.CreateModel(
            name='Utente',
            fields=[
                ('name', models.TextField(max_length=30)),
                ('surname', models.TextField(max_length=30)),
                ('CF', models.TextField(max_length=16, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='id_utente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locateBivacchi.Utente'),
        ),
    ]
