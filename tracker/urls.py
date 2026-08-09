from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('routine/<int:routine_id>/start/', views.start_workout, name='start_workout'),
    path('workout/<int:workout_id>/', views.active_workout, name='active_workout'),
    path('workout/<int:workout_id>/exercise/<int:exercise_id>/add/', views.add_set, name='add_set'),
    path('set/<int:set_id>/edit/', views.edit_set, name='edit_set'),
    path('set/<int:set_id>/delete/', views.delete_set, name='delete_set'),
    path('routine/<int:routine_id>/reorder/', views.update_exercise_order, name='reorder_exercises'),
    path('workout/<int:workout_id>/finish/', views.finish_workout, name='finish_workout'),
    path('forge/', views.forge, name='forge'),
    path('forge/craft/<int:recipe_id>/', views.craft_artifact, name='craft_artifact'),
]