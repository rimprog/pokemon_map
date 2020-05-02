from django.db import models


class PokemonElementType(models.Model):
    title = models.CharField('стихия', max_length=200)
    icon = models.ImageField('иконка', upload_to='elements_icons', null=True, blank=True)
    strong_against = models.ManyToManyField(
        'self',
        verbose_name='силен против',
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        return self.title


class Pokemon(models.Model):
    title = models.CharField('название RUS', max_length=200)
    title_en = models.CharField('название EN', max_length=200, blank=True)
    title_jp = models.CharField('название JP', max_length=200, blank=True)
    photo = models.ImageField('фото', upload_to='pokemons', null=True, blank=True)
    description = models.TextField('описание', blank=True)
    previous_evolution = models.ForeignKey(
        'self',
        verbose_name='из кого эволюционировал',
        related_name='next_evolutions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    element_types = models.ManyToManyField(
        PokemonElementType,
        verbose_name='стихия',
        related_name = 'pokemons',
        blank=True
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='покемон',
        related_name = 'pokemons_entities',
        on_delete=models.CASCADE
    )
    latitude = models.FloatField('широта')
    longitude = models.FloatField('долгота')
    appeared_at = models.DateTimeField('когда появился',  null=True, blank=True)
    disappeared_at = models.DateTimeField('когда исчезает',  null=True, blank=True)
    level = models.IntegerField('уровень',  null=True, blank=True)
    health = models.IntegerField('здоровье',  null=True, blank=True)
    strength = models.IntegerField('сила',  null=True, blank=True)
    defence = models.IntegerField('защита',  null=True, blank=True)
    stamina = models.IntegerField('выносливость',  null=True, blank=True)

    def __str__(self):
        return '{} широта:{} долгота:{}'.format(
            self.pokemon,
            self.latitude,
            self.longitude
        )
