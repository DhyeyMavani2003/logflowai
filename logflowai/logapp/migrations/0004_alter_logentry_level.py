# Generated by Django 5.1.6 on 2025-02-16 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logapp", "0003_alter_logentry_message"),
    ]

    operations = [
        migrations.AlterField(
            model_name="logentry",
            name="level",
            field=models.CharField(max_length=20, null=True),
        ),
    ]
