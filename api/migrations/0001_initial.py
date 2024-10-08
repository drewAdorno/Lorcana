# Generated by Django 4.1.1 on 2024-10-04 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('cost', models.IntegerField()),
                ('inkable', models.BooleanField(default=False)),
                ('lore', models.IntegerField(blank=True, null=True)),
                ('strength', models.IntegerField(blank=True, null=True)),
                ('willpower', models.IntegerField(blank=True, null=True)),
                ('rarity', models.CharField(blank=True, max_length=50, null=True)),
                ('card_type', models.CharField(blank=True, max_length=50, null=True)),
                ('artist', models.CharField(blank=True, max_length=255, null=True)),
                ('set_name', models.CharField(blank=True, max_length=100, null=True)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
