from django.contrib import admin
from .models import Exercise, Routine, WorkoutLog, SetLog

# Регистрируем наши модели, чтобы они появились в панели администратора
admin.site.register(Exercise)
admin.site.register(Routine)
admin.site.register(WorkoutLog)
admin.site.register(SetLog)