from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import Exercise, Routine, RoutineExercise

class Command(BaseCommand):
    help = 'Загружает тренировки для класса Воин из текстовых данных'

    def handle(self, *args, **options):
        # Данные для парсинга
        warrior_data = """
Пн Присед со свободной штангой для ног 1 - 75 - 10 2 - 75 - 10 3 - 75 - 10 4 - 75 - 10 Время передышки: 3 минуты
Жим гантелей на прямой скамье для груди 1 - 24 - 8 2 - 24 - 8 3 - 24 - 8 Время передышки: 3 минуты
Тяга верхнего блока для спины 1 - 79 - 10 2 - 79 - 10 3 - 79 - 10 Время передышки: 3 минуты
Армейский жим стоя со штангой для передней дельты 1 - 30 - 8 2 - 30 - 8 3 - 30 - 8 Время передышки: 3 минуты
Подъём локтей в тренажёре для средней дельты 1 - 41 - 10 2 - 41 - 10 3 - 41 - 10 Время передышки: 2 минуты
Ср Тяга штанги в наклоне для спины 1 - 50 - 8 2 - 50 - 8 3 - 50 - 8 Время передышки: 3 минуты
Отжимания на брусьях для трицепса и груди 1 - 0 - 10 2 - 0 - 10 3 - 0 - 10 Время передышки: 3 минуты
Гиперэкстензия с наклонной базой для спины 1 - 25 - 10 2 - 25 - 10 3 - 25 - 10 Время передышки: 2 минуты
Прогулка фермера с гантелями для предплечий и трапеции 1 - 24 - 1 (40 секунд) 2 - 24 - 1 (40 секунд) 3 - 24 - 1 (40 секунд) Время передышки: 2 минуты
Подъём гантелей в согнутом положении на заднюю дельту 1 - 8 - 10 2 - 8 - 10 3 - 8 - 10 Время передышки: 2 минуты
Скручивания на коврике для пресса 1 - 0 - 20 2 - 0 - 20 3 - 0 - 20 Время передышки: 1.5 минуты
Пт Присед со свободной штангой для ног 1 - 65 - 10 - легко, но так и должно быть на разминке 2 - 70 - 10 - чувствую напряжение в л колене и пояснице 3 - 70 - 10 Время передышки: 3 минуты
Жим гантелей на наклонной скамье 4 для верха груди 1 - 20 - 10 - напряжно 2 - 20 - 9 - мог сделать больше, жалею себя, напряжение чувствую в зубе 3 - 20 - 8 - мог сделать больше но самочувствие не позволило Время передышки: 3 минуты
Тяга верхнего блока для спины 1 - 79 - 10 2 - 79 - 7 - чувство бессилия 3 - 79 - 5 Время передышки: 3 минуты
Подъём грифа в смитте для икр 1 - 81 - 20 2 - 91 - 20 - напряжён 3 - 91 - 20 - аналогично Время передышки: 2 минуты
Молотки без упора для предплечий и бицепса 1 - 20 - 10 2 - 20 - 8 3 - 20 - 8 Время передышки: 2 минуты
        """.strip()

        # Получаем первого пользователя (для примера)
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('Нет пользователей в базе данных!'))
            return

        # Парсим данные по дням недели
        days_data = self.parse_workout_data(warrior_data)
        
        # Создаем тренировки для каждого дня
        for day_name, exercises in days_data.items():
            # Определяем основные группы мышц для дня
            muscle_groups = set()
            for exercise in exercises:
                # Убираем предлог "для" из названия группы мышц
                muscle_group = exercise['muscle_group'].replace(' для ', '').strip()
                muscle_groups.add(muscle_group)
            
            # Создаем название по группам мышц (отвечает на вопрос "что?")
            muscle_groups_list = sorted(list(muscle_groups))
            if muscle_groups_list:
                routine_name = " + ".join(muscle_groups_list[:3])  # Берем первые 3 группы
            else:
                routine_name = f"Воин - {day_name}"
            
            # Проверяем, существует ли уже такая тренировка
            if Routine.objects.filter(name=routine_name, hero_class='warrior', user=user).exists():
                self.stdout.write(self.style.WARNING(f'Тренировка "{routine_name}" уже существует, пропускаем'))
                continue
            
            # Создаем Routine
            routine = Routine.objects.create(
                name=routine_name,
                user=user,
                hero_class='warrior'
            )
            
            # Добавляем упражнения
            for idx, exercise_data in enumerate(exercises):
                exercise_name = exercise_data['name']
                muscle_group = exercise_data['muscle_group']
                
                # Создаем или получаем упражнение
                exercise, created = Exercise.objects.get_or_create(
                    name=exercise_name,
                    defaults={'muscle_group': muscle_group}
                )
                
                # Создаем связь RoutineExercise
                RoutineExercise.objects.create(
                    routine=routine,
                    exercise=exercise,
                    order=idx
                )
            
            self.stdout.write(self.style.SUCCESS(f'Создана тренировка: {routine_name} с {len(exercises)} упражнениями'))
        
        self.stdout.write(self.style.SUCCESS('Загрузка тренировок Воина завершена!'))

    def parse_workout_data(self, data):
        """Парсит текстовые данные тренировок"""
        days_data = {}
        current_day = None
        
        for line in data.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Определяем день недели
            if line.startswith('Пн'):
                current_day = 'Понедельник'
                days_data[current_day] = []
                line = line[2:].strip()
            elif line.startswith('Ср'):
                current_day = 'Среда'
                days_data[current_day] = []
                line = line[2:].strip()
            elif line.startswith('Пт'):
                current_day = 'Пятница'
                days_data[current_day] = []
                line = line[2:].strip()
            
            if current_day and line:
                # Парсим упражнение
                exercise_data = self.parse_exercise_line(line)
                if exercise_data:
                    days_data[current_day].append(exercise_data)
        
        return days_data

    def parse_exercise_line(self, line):
        """Парсит строку с упражнением"""
        # Ищем группу мышц (последние слова перед подходами)
        parts = line.split()
        
        # Находим индекс начала подходов (цифра - цифра - цифра)
        sets_start = -1
        for i, part in enumerate(parts):
            if part.isdigit() and i + 2 < len(parts):
                if parts[i + 1] == '-' and parts[i + 2].replace('.', '').isdigit():
                    sets_start = i
                    break
        
        if sets_start == -1:
            return None
        
        # Название упражнения и группа мышц
        exercise_part = ' '.join(parts[:sets_start])
        
        # Разделяем название и группу мышц
        if ' для ' in exercise_part:
            name_part, muscle_part = exercise_part.split(' для ', 1)
            exercise_name = name_part.strip()
            muscle_group = muscle_part.strip()
        else:
            exercise_name = exercise_part.strip()
            muscle_group = 'Разное'
        
        return {
            'name': exercise_name,
            'muscle_group': muscle_group
        }
