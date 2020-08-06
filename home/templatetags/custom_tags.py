from django.template.defaulttags import register


@register.filter
def get_name(user):
    try:
        name = user.userinfo.nick_name
    except:
        name = 'not_added'
    if name == 'not_added':
        name = user.first_name + " " + user.last_name
    if name == ' ':
        return user.username
    return name


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
