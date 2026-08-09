from django.db import migrations


def create_initial_recipes(apps, schema_editor):
    """Создание начальных рецептов для кузницы"""
    Recipe = apps.get_model('tracker', 'Recipe')
    RecipeIngredient = apps.get_model('tracker', 'RecipeIngredient')
    
    recipes_data = [
        {
            'name': 'Меч Тюра',
            'artifact_name': 'Легендарное оружие победы',
            'artifact_icon': '⚔️',
            'artifact_description': 'Меч, выкованный из самой сути победы. Гарантирует критический удар в бою.',
            'artifact_effect': 'Гарантированный критический удар',
            'effect_type': 'crit_chance',
            'effect_value': 100,
            'ingredients': [
                {'rune_name': 'Уруз (Сила)', 'quantity': 1},
                {'rune_name': 'Райдо (Путь)', 'quantity': 1},
                {'rune_name': 'Тейваз (Победа)', 'quantity': 1},
            ]
        },
        {
            'name': 'Кольцо Андвари',
            'artifact_name': 'Кольцо богатства',
            'artifact_icon': '💍',
            'artifact_description': 'Золотое кольцо, притягивающее опыт и знания.',
            'artifact_effect': '+50% к опыту за тренировку',
            'effect_type': 'xp_boost',
            'effect_value': 50,
            'ingredients': [
                {'rune_name': 'Феху (Богатство)', 'quantity': 2},
                {'rune_name': 'Вуньо (Триумф)', 'quantity': 1},
            ]
        },
        {
            'name': 'Секира Пробивания Плато',
            'artifact_name': 'Топор прорыва',
            'artifact_icon': '🪓',
            'artifact_description': 'Мощная секира, способная сокрушить любые плато в прогрессе.',
            'artifact_effect': 'Удвоение урона боссу',
            'effect_type': 'damage_boost',
            'effect_value': 100,
            'ingredients': [
                {'rune_name': 'Турисаз (Мощь)', 'quantity': 2},
                {'rune_name': 'Кеназ (Огонь)', 'quantity': 1},
                {'rune_name': 'Тейваз (Победа)', 'quantity': 1},
            ]
        },
        {
            'name': 'Щит Хеймдалля',
            'artifact_name': 'Щит защиты стрика',
            'artifact_icon': '🛡️',
            'artifact_description': 'Несокрушимый щит, хранящий ваш тренировочный стрик от пропусков.',
            'artifact_effect': 'Защита стрика от одного пропуска',
            'effect_type': 'streak_protection',
            'effect_value': 1,
            'ingredients': [
                {'rune_name': 'Альгиз (Защита)', 'quantity': 2},
                {'rune_name': 'Эйваз (Древо)', 'quantity': 1},
                {'rune_name': 'Гебо (Дар)', 'quantity': 1},
            ]
        },
        {
            'name': 'Амулет Воина',
            'artifact_name': 'Амулет силы',
            'artifact_icon': '📿',
            'artifact_description': 'Талисман, усиливающий все ваши удары.',
            'artifact_effect': '+25% к урону боссу',
            'effect_type': 'damage_boost',
            'effect_value': 25,
            'ingredients': [
                {'rune_name': 'Уруз (Сила)', 'quantity': 1},
                {'rune_name': 'Манназ (Человек)', 'quantity': 1},
            ]
        },
        {
            'name': 'Зелье Концентрации',
            'artifact_name': 'Эликсир фокуса',
            'artifact_icon': '🧪',
            'artifact_description': 'Магический эликсир, повышающий шанс критического удара.',
            'artifact_effect': '+25% шанс крита',
            'effect_type': 'crit_chance',
            'effect_value': 25,
            'ingredients': [
                {'rune_name': 'Ансуз (Мудрость)', 'quantity': 2},
                {'rune_name': 'Иса (Лед)', 'quantity': 1},
            ]
        },
        {
            'name': 'Баннер Победы',
            'artifact_name': 'Знамя триумфа',
            'artifact_icon': '🚩',
            'artifact_description': 'Боевой стяг, вдохновляющий на великие свершения.',
            'artifact_effect': '+30% к опыту',
            'effect_type': 'xp_boost',
            'effect_value': 30,
            'ingredients': [
                {'rune_name': 'Вуньо (Триумф)', 'quantity': 2},
                {'rune_name': 'Совилу (Солнце)', 'quantity': 1},
            ]
        },
        {
            'name': 'Клинок Имира',
            'artifact_name': 'Ледяной меч',
            'artifact_icon': '🗡️',
            'artifact_description': 'Меч из льда древнего великана. Наносит дополнительный урон.',
            'artifact_effect': '+50% к урону',
            'effect_type': 'damage_boost',
            'effect_value': 50,
            'ingredients': [
                {'rune_name': 'Кеназ (Огонь)', 'quantity': 2},
                {'rune_name': 'Иса (Лед)', 'quantity': 2},
            ]
        },
    ]
    
    for recipe_data in recipes_data:
        recipe = Recipe.objects.create(
            name=recipe_data['name'],
            artifact_name=recipe_data['artifact_name'],
            artifact_icon=recipe_data['artifact_icon'],
            artifact_description=recipe_data['artifact_description'],
            artifact_effect=recipe_data['artifact_effect'],
            effect_type=recipe_data['effect_type'],
            effect_value=recipe_data['effect_value'],
        )
        
        for ingredient_data in recipe_data['ingredients']:
            RecipeIngredient.objects.create(
                recipe=recipe,
                rune_name=ingredient_data['rune_name'],
                quantity_required=ingredient_data['quantity'],
            )


class Migration(migrations.Migration):
    dependencies = [
        ('tracker', '0008_recipe_artifact_recipeingredient'),
    ]

    operations = [
        migrations.RunPython(create_initial_recipes),
    ]
