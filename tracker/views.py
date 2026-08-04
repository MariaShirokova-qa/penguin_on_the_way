import json
import random
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Exercise, Routine, RoutineExercise, SetLog, WorkoutLog, Boss, HeroProfile, Achievement, HeroRune

from datetime import date, timedelta
from django.shortcuts import render

from django.utils.safestring import mark_safe


# Убедись, что модель Boss импортирована!

def home(request):
    routines = Routine.objects.all()
    # Учитываем твою логику связи через routine__user
    workouts = WorkoutLog.objects.filter(routine__user=request.user, completed=True)

    hero, _ = HeroProfile.objects.get_or_create(user=request.user)

    workout_dict = {}
    for w in workouts:
        d = w.date.date() if hasattr(w.date, 'date') else w.date
        workout_dict[d] = w

    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())

    week_days = []
    days_names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

    for i in range(7):
        current_day = start_of_week + timedelta(days=i)
        workout = workout_dict.get(current_day)

        week_days.append({
            'date': current_day,
            'day_name': days_names[i],
            'day_number': current_day.day,
            'is_today': current_day == today,
            'workout': workout,
        })

    boss, created = Boss.objects.get_or_create(
        user=request.user,
        defaults={'name': 'Ледяной Великан', 'max_hp': 1000, 'current_hp': 1000, 'level': 1}
    )


    # ЛОГИКА ШТРАФОВ ЗА ПРОПУСК ТРЕНИРОВКИ
    REQUIRED_DAYS = [0, 2, 4]  # 0=Пн, 2=Ср, 4=Пт
    today = date(2026, 8, 5)
    yesterday = today - timedelta(days=1)

    # Ключ для сессии, чтобы не лечить босса при каждом обновлении страницы
    penalty_key = f"boss_penalty_{yesterday.strftime('%Y-%m-%d')}"

    # Если вчера был обязательный день, и мы его еще не проверяли
    if yesterday.weekday() in REQUIRED_DAYS and not request.session.get(penalty_key):

        # Проверяем, есть ли тренировка за вчера в твоем workout_dict
        yesterday_workout = workout_dict.get(yesterday)

        # Если тренировки нет (или если есть поле completed и оно False)
        # Если у тебя в WorkoutLog нет поля completed, оставь просто `if not yesterday_workout:`
        if not yesterday_workout or not getattr(yesterday_workout, 'completed', True):
            boss.current_hp = min(boss.max_hp, boss.current_hp + 100)
            boss.save()

        # Ставим отметку в сессию: "За этот день проверка пройдена"
        request.session[penalty_key] = True
    # ==========================================

    return render(request, 'tracker/home.html', {
        'routines': routines,
        'week_days': week_days,
        'workouts': workouts,
        'boss': boss,
        'hero': hero,
    })


def start_workout(request, routine_id):
    # Находим выбранную программу
    routine = get_object_or_404(Routine, id=routine_id)

    # Создаем новую запись о тренировке в базе данных (фиксируем старт)
    workout_log = WorkoutLog.objects.create(user=request.user, routine=routine)

    # Перенаправляем на страницу активной тренировки (передаем ID созданной записи)
    return redirect('active_workout', workout_id=workout_log.id)


def active_workout(request, workout_id):
    workout_log = get_object_or_404(WorkoutLog, id=workout_id)

    # Создаем пустой список, куда сложим данные по каждому упражнению
    exercises_data = []

    for exercise in workout_log.routine.exercises.order_by('routineexercise__order'):
        # 1. Ищем прошлые подходы
        # Находим последнюю тренировку пользователя (кроме текущей), где он делал это упражнение
        last_workout = WorkoutLog.objects.filter(
            user=request.user,
            sets__exercise=exercise
        ).exclude(id=workout_log.id).order_by('-date').first()

        if last_workout:
            previous_sets = SetLog.objects.filter(workout_log=last_workout, exercise=exercise)
        else:
            previous_sets = None

        # 2. Ищем текущие подходы (которые мы только что ввели)
        current_sets = SetLog.objects.filter(workout_log=workout_log, exercise=exercise)

        # 3. Упаковываем всё вместе
        exercises_data.append({
            'exercise': exercise,
            'previous_sets': previous_sets,
            'current_sets': current_sets,
            'last_date': last_workout.date if last_workout else None,
        })

    return render(request, 'tracker/workout.html', {
        'workout_log': workout_log,
        'exercises_data': exercises_data
    })


def add_set(request, workout_id, exercise_id):
    if request.method == "POST":
        # Находим текущую тренировку и конкретное упражнение
        workout_log = get_object_or_404(WorkoutLog, id=workout_id)
        exercise = get_object_or_404(Exercise, id=exercise_id)

        # Получаем данные из формы (вес и повторения)
        weight = request.POST.get('weight')
        reps = request.POST.get('reps')

        # Сохраняем подход в базу данных
        SetLog.objects.create(
            workout_log=workout_log,
            exercise=exercise,
            weight=weight,
            reps=reps
        )

        # Сразу возвращаем пользователя обратно на страницу тренировки
        return redirect('active_workout', workout_id=workout_id)


def edit_set(request, set_id):
    # Находим нужный подход в базе
    set_log = get_object_or_404(SetLog, id=set_id)

    if request.method == "POST":
        # Если форма отправлена, обновляем данные
        set_log.weight = request.POST.get('weight')
        set_log.reps = request.POST.get('reps')
        set_log.save()

        # Возвращаемся обратно на экран тренировки
        return redirect('active_workout', workout_id=set_log.workout_log.id)

    # Если это обычный переход по ссылке — показываем страницу с формой
    return render(request, 'tracker/edit_set.html', {'set_log': set_log})


def delete_set(request, set_id):
    # Находим подход
    set_log = get_object_or_404(SetLog, id=set_id)
    # Запоминаем ID тренировки, чтобы знать, куда возвращаться
    workout_id = set_log.workout_log.id

    # Удаляем только если пришел POST-запрос (нажата кнопка)
    if request.method == "POST":
        set_log.delete()

    return redirect('active_workout', workout_id=workout_id)

def update_exercise_order(request, routine_id):
    if request.method == 'POST':
        # Получаем данные от JavaScript
        data = json.loads(request.body)
        order_list = data.get('order', [])

        # Обновляем порядок каждого упражнения в базе
        for index, exercise_id in enumerate(order_list):
            RoutineExercise.objects.filter(
                routine_id=routine_id,
                exercise_id=exercise_id
            ).update(order=index)

        return JsonResponse({'status': 'success'})


# Список рун, которые могут выпасть (разместите его перед функцией)
AVAILABLE_RUNES = [
    # === 1. Этт Фрейра (Материальное и физическое) ===
    ("ᚠ", "Феху (Богатство)", "Символ золота и изобилия. Понадобится в Кузнице для создания 'Кольца Андвари' (бонус к опыту)."),
    ("ᚢ", "Уруз (Сила)", "Первобытная энергия дикого быка. Ключевой компонент для крафта тяжелой брони."),
    ("ᚦ", "Турисаз (Мощь)", "Удар молота Тора. Сохраните её, чтобы выковать 'Секиру Пробивания Плато'."),
    ("ᚨ", "Ансуз (Мудрость)", "Дыхание Одина. Используется для создания зелий концентрации."),
    ("ᚱ", "Райдо (Путь)", "Колесо телеги. Незаменима для артефактов, ускоряющих восстановление после тренировок."),
    ("ᚲ", "Кеназ (Огонь)", "Внутреннее пламя. Освещает путь и сжигает калории. Нужна для 'Клинка Имира'."),
    ("ᚷ", "Гебо (Дар)", "Руна баланса. Соединяет несовместимые стихии при сложном крафте."),
    ("ᚹ", "Вуньо (Триумф)", "Радость победы. Вплетается в знамена и дарует титулы."),

    # === 2. Этт Хеймдалля (Преодоление и стойкость) ===
    ("ᚺ", "Хагалаз (Разрушение)", "Разрушение старых привычек и слабостей. Очищает слот для мощных чар."),
    ("ᚾ", "Наутиз (Преодоление)", "Выносливость в трудные моменты. Закаляет волю в период тяжелых нагрузок."),
    ("ᛁ", "Иса (Лед)", "Холодный рассудок и концентрация. Нужна для защиты от ментальной усталости."),
    ("ᛃ", "Йера (Урожай)", "Награда за регулярный труд. Умножает количество получаемых ресурсов."),
    ("ᛇ", "Эйваз (Древо)", "Стойкость Иггдрасиля. Крепкий стержень и защита суставов от травм."),
    ("ᛈ", "Перто (Судьба)", "Скрытый потенциал. Позволяет заглянуть за грани возможностей во время подходов."),
    ("ᛉ", "Альгиз (Защита)", "Щит Хеймдалля. Оберегает воительницу от выгорания и спасает стрик."),
    ("ᛋ", "Совилу (Солнце)", "Энергия светила. Заряжает тело взрывной силой перед тяжелой тренировкой."),

    # === 3. Этт Тюра (Дух и разум) ===
    ("ᛏ", "Тейваз (Победа)", "Копье Тюра. Главный элемент для создания легендарного оружия победы."),
    ("ᛒ", "Беркана (Рост)", "Возрождение и обновление тела. Ускоряет мышечное восстановление после сна."),
    ("ᛖ", "Эваз (Прогресс)", "Движение вперед без остановок. Увеличивает темп и продуктивность сессии."),
    ("ᛗ", "Манназ (Человек)", "Самосовершенствование. Помогает превзойти свои прошлые рекорды."),
    ("ᛚ", "Лагуз (Поток)", "Гибкость и адаптация. Помогает легко переносить смену программы тренировок."),
    ("ᛜ", "Ингуз (Энергия)", "Внутреннее семя силы. Накапливает энергию для финального рывка в упражнении."),
    ("ᛞ", "Дагаз (Прорыв)", "Рассвет и трансформация. Символ перехода на новый уровень физической формы."),
    ("ᛟ", "Одал (Наследие)", "Родовая память. Закрепляет достигнутый результат навечно в вашем профиле.")
]


def update_streak_and_achievements(hero_profile):
    """
    Выдает 1 случайную руну за каждую тренировку и проверяет стрик для Титулов.
    Возвращает HTML-строку с сообщением о луте.
    """
    today = date.today()
    loot_message = ""

    # === 1. ФАРМ РУН (Срабатывает ВСЕГДА, без ограничений) ===
    icon, name, desc = random.choice(AVAILABLE_RUNES)

    hero_rune, created = HeroRune.objects.get_or_create(
        hero=hero_profile,
        name=name,
        # Добавили description в defaults!
        defaults={'icon': icon, 'quantity': 0, 'description': desc}
    )
    hero_rune.quantity += 1
    # Если руна уже была, на всякий случай обновляем её описание на самое свежее из списка
    hero_rune.description = desc
    hero_rune.save()

    # Добавляем в сообщение информацию о выпавшей руне
    loot_message += f"<br><br><span style='color: inherit; font-size: 0.9 rem;'>✨ Выбита руна: {icon} {name}!</span>"

    # === 2. ПРОВЕРКА СТРИКА (Срабатывает только 1 раз в день) ===
    if hero_profile.last_workout_date != today:
        # Если сегодня тренировок еще не было, считаем дни
        if hero_profile.last_workout_date:
            delta_days = (today - hero_profile.last_workout_date).days

            if delta_days <= 3:
                hero_profile.current_streak += 1
            else:
                hero_profile.current_streak = 1  # Костер потух, начинаем заново
        else:
            hero_profile.current_streak = 1

        hero_profile.last_workout_date = today
        hero_profile.save()

    # === 3. ПУТЬ НА АСГАРД (Выдача Титулов) ===
    rewards = {
        7: ("🛡️", "Звание: Страж Предела", "Первое испытание пройдено. Костер разведен."),
        21: ("🪓", "Титул: Берсерк", "Тело привыкло к стали. Дисциплина крепчает."),
        45: ("🦅", "Звание: Ворон Одина", "Тренировки стали вашей истинной природой."),
        90: ("⚡", "Титул: Эйнхерий", "Легендарный статус. Вы достойны залов Вальхаллы!"),
        180: ("❄️", "Гроза Ётунов", "Боссы дрожат при одном вашем виде.")
    }

    if hero_profile.current_streak in rewards:
        t_icon, t_name, t_desc = rewards[hero_profile.current_streak]

        if not Achievement.objects.filter(hero=hero_profile, name=t_name).exists():
            Achievement.objects.create(hero=hero_profile, icon=t_icon, name=t_name, description=t_desc)
            # Добавляем приписку о новом титуле к сообщению о руне
            loot_message += f"<br><span class='viking-reward' style='color: var(--sand, #e2e1d8); font-weight: bold;'>📜 Получен великий титул: {t_icon} {t_name}!</span>"

    return loot_message

def finish_workout(request, workout_id):
    # 1. Получаем текущую тренировку
    workout = get_object_or_404(WorkoutLog, id=workout_id)

    workout.completed = True
    workout.save()

    # 1. Получаем или создаем профиль героя
    hero, created = HeroProfile.objects.get_or_create(user=request.user)

    base_xp = 100
    bonus_xp = 0

    # 2. Анализируем прогрессию нагрузок для бонусов
    current_sets = SetLog.objects.filter(workout_log=workout)

    for current_set in current_sets:
        # Ищем лучший подход в этом же упражнении из прошлых завершенных тренировок
        prev_best_set = SetLog.objects.filter(
            workout_log__routine__user=request.user,
            exercise=current_set.exercise,
            workout_log__date__lt=workout.date,
            workout_log__completed=True
        ).order_by('-weight', '-reps').first()

        if prev_best_set:
            if current_set.weight > prev_best_set.weight:
                bonus_xp += 50  # Бонус за рост рабочего веса
            elif current_set.weight == prev_best_set.weight and current_set.reps > prev_best_set.reps:
                bonus_xp += 25  # Бонус за рост выносливости (повторений)

    # 3. Начисляем опыт и сохраняем
    total_xp_gained = base_xp + bonus_xp
    hero.experience += total_xp_gained
    hero.save()

    # 2. Получаем Босса
    boss = Boss.objects.get(user=request.user)

    # 3. Базовый урон
    base_damage = 50
    bonus_damage = 0

    # 4. Расчет бонуса за прогресс весов (Критический урон)
    current_sets = SetLog.objects.filter(workout_log=workout)

    # Находим максимальный вес для каждого упражнения на этой тренировке
    current_max_weights = {}
    for s in current_sets:
        if s.weight is not None:
            if s.exercise.id not in current_max_weights or s.weight > current_max_weights[s.exercise.id]:
                current_max_weights[s.exercise.id] = s.weight

    # Сравниваем с прошлыми тренировками
    for exercise_id, current_max in current_max_weights.items():
        # Ищем максимальный вес для этого упражнения СТРОГО до сегодняшней даты
        prev_max_set = SetLog.objects.filter(
            workout_log__routine__user=request.user,
            exercise_id=exercise_id,
            workout_log__date__lt=workout.date
        ).order_by('-weight').first()

        # Если раньше это упражнение делали и сейчас вес больше — даем бонус!
        if prev_max_set and prev_max_set.weight is not None:
            if current_max > prev_max_set.weight:
                bonus_damage += 10

    total_damage = base_damage + bonus_damage

    # 5. Наносим урон боссу
    boss.current_hp -= total_damage

    # Формируем сообщение об уроне
    boss_message = f" ⚔️ Ты нанесла {total_damage} урона боссу {boss.name}!"
    if bonus_damage > 0:
        boss_message += f" (Из них {bonus_damage} — критический урон за новые рекорды!)"

    # 6. Проверка на смерть босса
    if boss.current_hp <= 0:
        boss.level += 1
        boss.max_hp += 200  # Босс становится жирнее
        boss.current_hp = boss.max_hp
        boss_message += f" 👹 Враг пал! {boss.name} переходит на {boss.level} уровень и становится сильнее!"

    boss.save()

    achievement_msg = update_streak_and_achievements(hero)

    # 7. Наш арсенал средневековых мотиваций
    quotes = [
        "Твой дух выкован из лучшей стали. Славный бой с железом окончен, воительница!",
        "Доспехи тяжелы, но твоя решимость крепче. Сегодня ты одержала еще одну великую победу!",
        "Меч куется в огне и ударах кузнечного молота, а сила — в преодолении. Ты справилась, дева-воин!",
        "Даже самые прочные крепостные стены рушатся, но твоя воля непоколебима.",
        "Пусть менестрели сложат песни о твоем упорстве. Тренировка завершена достойно!",
        "Ты не просто подняла тяжесть, ты бросила вызов гравитации и победила, как истинная королева Севера!"
    ]

    quote = random.choice(quotes)
    styled_quote = f"<span style='font-style: italic; font-size: 1.1rem; color: #f8f9fa;'>{quote}</span>"

    # 1. Формируем чистую строку про полученный опыт
    xp_message = f"✨ Получено {total_xp_gained} XP (из них {bonus_xp} за рекорды)."

    # 2. Собираем текст
    final_message = mark_safe(
        f"{styled_quote}<br><br>"
        f"{xp_message}<br>"
        f"{boss_message}"
        f"{achievement_msg}"
    )

    messages.success(request, final_message)
    return redirect('home')