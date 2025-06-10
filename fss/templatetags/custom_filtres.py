from django import template

register = template.Library()

@register.filter
def initials(user):
    if not user:
        return ""
    last = user.last_name or ""
    first = user.first_name[0] + '.' if user.first_name else ""
    patronymic = user.patronymic[0] + '.' if hasattr(user, 'patronymic') and user.patronymic else ""
    return f"{last}.{first}{patronymic}"


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)