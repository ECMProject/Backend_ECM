# Generated by Django 3.2.23 on 2024-02-11 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eseme', '0006_auto_20231230_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='memb_role',
            field=models.IntegerField(default=1),
        ),
    ]