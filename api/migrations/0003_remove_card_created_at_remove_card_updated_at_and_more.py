# Generated by Django 4.1.1 on 2024-10-04 03:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_deck'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='card',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='deck',
            name='cards',
        ),
        migrations.CreateModel(
            name='DeckCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.card')),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.deck')),
            ],
            options={
                'unique_together': {('deck', 'card')},
            },
        ),
    ]
