# Generated by Django 2.0.6 on 2018-11-17 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locateBivacchi', '0007_auto_20181117_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bivacco',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]