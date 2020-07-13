from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_name(user):
    name = user.first_name + " " + user.last_name
    if name == ' ':
        return user.username
    return name
