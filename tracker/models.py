from django.db import models
from django.contrib.auth.models import User

# 1. Справочник упражнений
class Exercise(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название упражнения")
    muscle_group = models.CharField(max_length=50, blank=True, null=True, verbose_name="Группа мышц")

    def __str__(self):
        return self.name

# 2. Шаблон тренировки (Например, "Грудь + Трицепс")
class Routine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField(max_length=100, verbose_name="Название программы")
    # Указываем Django использовать нашу новую промежуточную таблицу:
    exercises = models.ManyToManyField(Exercise, through='RoutineExercise', verbose_name="Упражнения")

    def __str__(self):
        return f"{self.name} ({self.user.username})"

# НОВАЯ ПРОМЕЖУТОЧНАЯ ТАБЛИЦА
class RoutineExercise(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        # Указываем базе данных всегда сортировать по этому полю
        ordering = ['order']

    def __str__(self):
        return f"{self.routine.name} - {self.exercise.name}"

# 3. Запись конкретного дня тренировки
class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    routine = models.ForeignKey(Routine, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Программа")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время")

    def __str__(self):
        return f"Тренировка {self.date.strftime('%Y-%m-%d')} - {self.user.username}"

# 4. Выполненный подход
class SetLog(models.Model):
    workout_log = models.ForeignKey(WorkoutLog, on_delete=models.CASCADE, related_name='sets')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, verbose_name="Упражнение")
    weight = models.DecimalField(max_digits=5, decimal_places=1, verbose_name="Вес (кг)")
    reps = models.IntegerField(verbose_name="Повторения")
    order = models.IntegerField(default=1, verbose_name="Порядковый номер подхода")

    def __str__(self):
        return f"{self.exercise.name}: {self.weight}кг x {self.reps}"