# Generated by Django 5.0.3 on 2024-03-17 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thinkpart', '0009_rename_part_old_userreplacedpart_part_original'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userreplacedpart',
            name='comment',
            field=models.TextField(),
        ),
    ]