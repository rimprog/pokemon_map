# Generated by Django 2.2.3 on 2020-05-02 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0015_auto_20200502_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='element_types',
            field=models.ManyToManyField(blank=True, null=True, to='pokemon_entities.PokemonElementType', verbose_name='стихия'),
        ),
    ]