# Generated by Django 4.2.6 on 2023-10-18 16:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_quote_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additional_costs',
            name='id',
            field=models.UUIDField(default=uuid.UUID('6f6e5535-0c40-4ea4-918e-64410dae159d'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='base_coverage',
            name='id',
            field=models.UUIDField(default=uuid.UUID('cba23d46-ab97-483f-a9de-c33860733176'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='quote',
            name='id',
            field=models.UUIDField(default=uuid.UUID('1a44967e-e1a7-4501-bc54-0875ccad7d60'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='state',
            name='id',
            field=models.UUIDField(default=uuid.UUID('edb8f781-d1a9-45c4-bca2-519a8053ab5c'), primary_key=True, serialize=False),
        ),
    ]
