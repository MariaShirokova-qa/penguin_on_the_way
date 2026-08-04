from django.contrib import admin
from django.db import models  # НОВЫЙ ИМПОРТ: нужен, чтобы сослаться на IntegerField
from django.forms import NumberInput  # НОВЫЙ ИМПОРТ: нужен для управления HTML-инпутом
from .models import Exercise, Routine, RoutineExercise, WorkoutLog, SetLog, HeroProfile, Boss, Achievement, HeroRune


class RoutineExerciseInline(admin.TabularInline):
    model = RoutineExercise
    extra = 1

    # МАГИЯ ЗДЕСЬ: Указываем Django, что для всех целых чисел нужен HTML-атрибут min="0"
    formfield_overrides = {
        models.IntegerField: {'widget': NumberInput(attrs={'min': '0'})},
    }


class RoutineAdmin(admin.ModelAdmin):
    inlines = [RoutineExerciseInline]


admin.site.register(Exercise)
admin.site.register(Routine, RoutineAdmin)
admin.site.register(WorkoutLog)
admin.site.register(SetLog)
admin.site.register(HeroProfile)
admin.site.register(Boss)
admin.site.register(Achievement)
admin.site.register(HeroRune)

