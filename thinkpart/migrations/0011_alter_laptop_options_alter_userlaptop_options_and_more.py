# Generated by Django 5.0.3 on 2024-03-20 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thinkpart', '0010_alter_userreplacedpart_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='laptop',
            options={'ordering': ['year']},
        ),
        migrations.AlterModelOptions(
            name='userlaptop',
            options={'ordering': ['-purchased']},
        ),
        migrations.AlterModelOptions(
            name='userreplacedpart',
            options={'ordering': ['-date']},
        ),
    ]
