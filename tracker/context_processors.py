from .models import HeroProfile

def hero_context(request):
    """Добавляет hero_profile в контекст всех шаблонов"""
    if request.user.is_authenticated:
        try:
            hero = HeroProfile.objects.get(user=request.user)
            return {'hero': hero}
        except HeroProfile.DoesNotExist:
            return {'hero': None}
    return {'hero': None}
