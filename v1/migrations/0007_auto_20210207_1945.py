# Generated by Django 2.2.6 on 2021-02-08 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0006_rating_time_elapsed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respondent',
            name='product_seq',
            field=models.CharField(default='None', max_length=150),
        ),
    ]