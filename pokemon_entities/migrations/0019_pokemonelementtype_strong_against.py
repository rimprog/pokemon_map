# Generated by Django 2.2.3 on 2020-05-02 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0018_auto_20200502_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonelementtype',
            name='strong_against',
            field=models.ManyToManyField(blank=True, related_name='_pokemonelementtype_strong_against_+', to='pokemon_entities.PokemonElementType', verbose_name='силен против'),
        ),
    ]