import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import PokemonEntity
from .models import Pokemon

import folium


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, pokemon_entity_info_html, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name.encode('ascii', errors='xmlcharrefreplace').decode('utf-8'),
        icon=icon,
        popup=pokemon_entity_info_html.encode('ascii', errors='xmlcharrefreplace').decode('utf-8')
    ).add_to(folium_map)


def prepare_pokemon_entity_info_html(pokemon_entity):
    pokemon_entity_info_html = """
        <h3> Характеристики покемона:</h3>
        <p>Появился: {appeared_at}</p>
        <p>Исчезнет: {disappeared_at}</p>
        <p>Уровень: {level}</p>
        <p>Здоровье: {health}</p>
        <p>Сила: {strength}</p>
        <p>Защита: {defence}</p>
        <p>Выносливость: {stamina}</p>
        """.format(
                appeared_at=pokemon_entity.appeared_at,
                disappeared_at=pokemon_entity.disappeared_at,
                level=pokemon_entity.level,
                health=pokemon_entity.health,
                strength=pokemon_entity.strength,
                defence=pokemon_entity.defence,
                stamina=pokemon_entity.stamina
            )

    return pokemon_entity_info_html


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemons_entities = PokemonEntity.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.latitude,
            pokemon_entity.longitude,
            pokemon_entity.pokemon.title,
            prepare_pokemon_entity_info_html(pokemon_entity),
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url) if pokemon_entity.pokemon.photo else DEFAULT_IMAGE_URL
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.photo.url if pokemon.photo else DEFAULT_IMAGE_URL,
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    except Http404:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemons_entities = pokemon.pokemons_entities.all()
    for pokemon_entity in pokemons_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.latitude,
            pokemon_entity.longitude,
            pokemon_entity.pokemon.title,
            prepare_pokemon_entity_info_html(pokemon_entity),
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url) if pokemon_entity.pokemon.photo else DEFAULT_IMAGE_URL
        )

    requested_pokemon = {
        "pokemon_id": pokemon.id,
        "title_ru": pokemon.title,
        "title_en": pokemon.title_en,
        "title_jp": pokemon.title_jp,
        "description": pokemon.description,
        "img_url": pokemon.photo.url if pokemon.photo else DEFAULT_IMAGE_URL,
    }

    if pokemon.previous_evolution:
        requested_pokemon["previous_evolution"] = {
            "title_ru": pokemon.previous_evolution.title,
            "pokemon_id": pokemon.previous_evolution.id,
            "img_url": pokemon.previous_evolution.photo.url if pokemon.previous_evolution.photo else DEFAULT_IMAGE_URL
        }

    if pokemon.next_evolutions.count() > 0:
        next_evolution = pokemon.next_evolutions.all()[0]
        requested_pokemon["next_evolution"] = {
            "title_ru": next_evolution.title,
            "pokemon_id": next_evolution.id,
            "img_url": next_evolution.photo.url if next_evolution.photo else DEFAULT_IMAGE_URL
        }

    pokemon_element_types = []
    for pokemon_element_type in pokemon.element_types.all():
        pokemon_element_type = {
            'title': pokemon_element_type.title,
            'img': request.build_absolute_uri(pokemon_element_type.icon.url) if pokemon_element_type.icon else DEFAULT_IMAGE_URL
        }
        pokemon_element_types.append(pokemon_element_type)

    requested_pokemon["element_types"] = pokemon_element_types

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': requested_pokemon})
