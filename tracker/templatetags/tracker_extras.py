from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Кастомный фильтр для доступа к элементам словаря по ключу в Django шаблоне
    Использование: {{ mydict|get_item:key }}
    """
    return dictionary.get(key)
