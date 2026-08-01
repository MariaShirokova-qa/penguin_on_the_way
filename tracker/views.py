from datetime import date, timedelta
import json
import random
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Exercise, Routine, RoutineExercise, SetLog, WorkoutLog


def home(request):
    routines = Routine.objects.all()
    workouts = WorkoutLog.objects.filter(routine__user=request.user)

    # ИСПРАВЛЕНИЕ: Превращаем дату-время в чистую дату (w.date извлекается как дата или дата-время, берем .date() если это datetime)
    workout_dict = {}
    for w in workouts:
        # Если w.date — это datetime, берем .date(), если уже date — оставляем как есть
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

    return render(request, 'tracker/home.html', {
        'routines': routines,
        'week_days': week_days,
        'workouts': workouts,
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

def finish_workout(request, workout_id):
    # Наш арсенал средневековых мотиваций
    quotes = [
        "Твой дух выкован из лучшей стали. Славный бой с железом окончен, воительница!",
        "Доспехи тяжелы, но твоя решимость крепче. Сегодня ты одержала еще одну великую победу!",
        "Меч куется в огне и ударах кузнечного молота, а сила — в преодолении. Ты справилась, дева-воин!",
        "Даже самые прочные крепостные стены рушатся, но твоя воля непоколебима.",
        "Пусть менестрели сложат песни о твоем упорстве. Тренировка завершена достойно!",
        "Ты не просто подняла тяжесть, ты бросила вызов гравитации и победила, как истинная королева Севера!"
    ]

    # Прикрепляем случайную фразу к сообщению об успехе
    messages.success(request, random.choice(quotes))

    # Возвращаем на главную страницу
    return redirect('home')