# Generated by Django 4.1.1 on 2024-10-04 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_card_ink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='ink',
        ),
        migrations.AddField(
            model_name='card',
            name='color',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
