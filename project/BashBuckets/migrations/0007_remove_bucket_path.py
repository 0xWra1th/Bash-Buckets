# Generated by Django 3.2 on 2021-06-07 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BashBuckets', '0006_alter_user_usage_limit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bucket',
            name='path',
        ),
    ]
