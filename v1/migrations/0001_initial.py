# Generated by Django 2.2.6 on 2021-01-26 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Respondent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos_key', models.PositiveSmallIntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('mturk_id', models.CharField(default='None', max_length=50)),
            ],
        ),
    ]