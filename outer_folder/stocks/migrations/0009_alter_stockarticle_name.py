# Generated by Django 3.2.4 on 2022-02-16 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0008_auto_20220128_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockarticle',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]