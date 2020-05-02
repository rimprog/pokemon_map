from django.contrib import admin

from .models import Pokemon
from .models import PokemonEntity
from .models import PokemonElementType


admin.site.register(Pokemon)
admin.site.register(PokemonEntity)
admin.site.register(PokemonElementType)
