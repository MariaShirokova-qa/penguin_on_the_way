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
    completed = models.BooleanField(default=False)

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


class Boss(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='boss')
    name = models.CharField(max_length=100, default='Ледяной Великан')
    level = models.IntegerField(default=1)
    max_hp = models.IntegerField(default=1000)
    current_hp = models.IntegerField(default=1000)

    class Meta:
        verbose_name = "Boss"
        verbose_name_plural = "Bosses"

    def __str__(self):
        return f"{self.name} (Ур. {self.level}) - {self.user.username}"

    @property
    def hp_percentage(self):
        if self.max_hp > 0:
            return int((self.current_hp / self.max_hp) * 100)
        return 0

class HeroProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hero_profile')

    # Физические параметры и цели
    current_weight = models.DecimalField(max_digits=5, decimal_places=1, default=61.0, verbose_name="Текущий вес")
    main_goal = models.CharField(max_length=200, default="Крылья и песочные часы",
                                 verbose_name="Главная цель")
    target_muscles = models.CharField(max_length=200, default="Спина, Ягодицы, Плечи",
                                      verbose_name="Акцентные мышцы")

    # XP
    experience = models.IntegerField(default=0, verbose_name="Опыт (XP)")

    # Стрики
    current_streak = models.IntegerField(default=0, verbose_name="Текущий стрик")
    last_workout_date = models.DateField(null=True, blank=True, verbose_name="Дата последней тренировки")

    @property
    def level(self):
        # 1000 XP = 1 уровень. Начинаем с 1 уровня.
        return (self.experience // 1000) + 1

    @property
    def current_level_xp(self):
        # Сколько опыта получено на текущем уровне
        return self.experience % 1000

    @property
    def xp_percentage(self):
        # Процент заполнения полоски опыта (от 0 до 100)
        return int((self.current_level_xp / 1000) * 100)

    def __str__(self):
        return f"Герой {self.user.username} - Уровень {self.level}"


# 2. Инвентарь (Наград)
class Achievement(models.Model):
    hero = models.ForeignKey(HeroProfile, on_delete=models.CASCADE, related_name='achievements')
    name = models.CharField(max_length=100, verbose_name="Название руны/титула")
    icon = models.CharField(max_length=50, verbose_name="Иконка (Эмодзи)")
    description = models.TextField(verbose_name="Описание подвига")
    unlocked_at = models.DateField(auto_now_add=True, verbose_name="Дата получения")

    def __str__(self):
        return f"{self.icon} {self.name} ({self.hero.user.username})"

# НОВАЯ Мешок для рун
class HeroRune(models.Model):
    hero = models.ForeignKey(HeroProfile, on_delete=models.CASCADE, related_name='runes')
    name = models.CharField(max_length=50, verbose_name="Название руны")
    icon = models.CharField(max_length=10, verbose_name="Символ")
    quantity = models.IntegerField(default=1, verbose_name="Количество") # Считаем штуки!
    description = models.TextField(verbose_name="Описание и лор", default="Сила этой руны пока не раскрыта.")

    def __str__(self):
        return f"{self.icon} {self.name} x{self.quantity} ({self.hero.user.username})"