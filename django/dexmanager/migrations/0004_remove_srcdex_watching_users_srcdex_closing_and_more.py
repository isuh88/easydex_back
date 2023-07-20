# Generated by Django 4.2 on 2023-07-14 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dexmanager', '0003_rename_dex_userdex_srcdex'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='srcdex',
            name='watching_users',
        ),
        migrations.AddField(
            model_name='srcdex',
            name='closing',
            field=models.CharField(default='1000', max_length=256),
        ),
        migrations.AlterField(
            model_name='srcdex',
            name='values',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
