# Generated by Django 2.2.6 on 2021-02-02 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0004_auto_20210131_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='amazon_id',
            field=models.CharField(default='None', max_length=50),
        ),
    ]