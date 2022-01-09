# Generated by Django 3.2.4 on 2022-01-09 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0005_auto_20220109_0250'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pricedata',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='stocksymbol',
            name='name',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
