# Generated by Django 3.0.6 on 2021-01-22 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0002_auto_20210122_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='amountpaid',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
