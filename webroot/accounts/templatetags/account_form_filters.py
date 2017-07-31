# from django import template
# register = template.Library()
#
# @register.filter('fieldtype')
# def fieldtype(field):
#     return field.field.widget.__class__.__name__

from django import template
register = template.Library()

@register.filter('klass')
def klass(ob):
    return ob.__class__.__name__
