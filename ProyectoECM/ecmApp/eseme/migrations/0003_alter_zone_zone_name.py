# Generated by Django 4.2.1 on 2023-12-09 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eseme', '0002_remove_zone_zone_description_zone_zone_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zone',
            name='zone_name',
            field=models.CharField(max_length=20),
        ),
    ]
