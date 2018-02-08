from django import template

register = template.Library()

@register.filter
def format_for_google(quoted_null_string):
    return quoted_null_string.replace("'", '').replace("None","null")