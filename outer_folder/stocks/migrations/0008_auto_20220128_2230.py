# Generated by Django 3.2.4 on 2022-01-29 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0007_auto_20220128_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockarticle',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='stockgainer',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='stockloser',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
