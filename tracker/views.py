from django.shortcuts import render, redirect, get_object_or_404
from .models import Routine, WorkoutLog, Exercise, SetLog

def home(request):
    routines = Routine.objects.all()
    return render(request, 'tracker/home.html', {'routines': routines})


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

    for exercise in workout_log.routine.exercises.all():
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