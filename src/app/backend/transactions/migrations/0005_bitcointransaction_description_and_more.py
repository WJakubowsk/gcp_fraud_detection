# Generated by Django 5.0.4 on 2024-05-15 12:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "transactions",
            "0004_rename_aggregate_feature_1_bitcointransaction_aggregate_feature_1_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="bitcointransaction",
            name="description",
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="bitcointransaction",
            name="date",
            field=models.DateTimeField(),
        ),
    ]
