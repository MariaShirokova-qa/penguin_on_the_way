"""Сервисы для бизнес-логики приложения"""

from .models import HeroProfile, Artifact


class ArtifactService:
    """Сервис для работы с артефактами"""
    
    @staticmethod
    def get_active_artifacts(hero: HeroProfile):
        """Получить все активные артефакты героя"""
        return hero.artifacts.filter(is_active=True)
    
    @staticmethod
    def calculate_artifact_bonuses(hero: HeroProfile):
        """Рассчитать бонусы от активных артефактов"""
        active_artifacts = ArtifactService.get_active_artifacts(hero)
        
        bonuses = {
            'crit_chance': 0,
            'damage_boost': 0,
            'xp_boost': 0,
            'streak_protection': 0
        }
        
        for artifact in active_artifacts:
            if artifact.effect_type in bonuses:
                bonuses[artifact.effect_type] += artifact.effect_value
        
        return bonuses
    
    @staticmethod
    def apply_damage_bonus(base_damage: int, hero: HeroProfile) -> int:
        """Применить бонус урона от артефактов"""
        bonuses = ArtifactService.calculate_artifact_bonuses(hero)
        return base_damage + bonuses['damage_boost']
    
    @staticmethod
    def apply_xp_bonus(base_xp: int, hero: HeroProfile) -> int:
        """Применить бонус опыта от артефактов"""
        bonuses = ArtifactService.calculate_artifact_bonuses(hero)
        if bonuses['xp_boost'] > 0:
            bonus = int(base_xp * bonuses['xp_boost'] / 100)
            return base_xp + bonus
        return base_xp
    
    @staticmethod
    def has_streak_protection(hero: HeroProfile) -> bool:
        """Проверить, есть ли у героя защита стрика"""
        bonuses = ArtifactService.calculate_artifact_bonuses(hero)
        return bonuses['streak_protection'] > 0
    
    @staticmethod
    def consume_streak_protection(hero: HeroProfile):
        """Использовать защиту стрика (если есть активный артефакт)"""
        active_artifacts = ArtifactService.get_active_artifacts(hero)
        for artifact in active_artifacts:
            if artifact.effect_type == 'streak_protection' and artifact.effect_value > 0:
                artifact.effect_value -= 1
                if artifact.effect_value == 0:
                    artifact.is_active = False
                artifact.save()
                return True
        return False
