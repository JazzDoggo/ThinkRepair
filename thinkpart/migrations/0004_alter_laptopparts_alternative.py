# Generated by Django 5.0.3 on 2024-03-14 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thinkpart', '0003_alter_part_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laptopparts',
            name='alternative',
            field=models.ManyToManyField(blank=True, related_name='alternative_part', to='thinkpart.part'),
        ),
    ]
