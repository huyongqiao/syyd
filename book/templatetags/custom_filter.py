from django import template

from book.utils import category_rev_map

register = template.Library()

@register.filter
def hanzi_pinyin(hanzi):
    try:
        return category_rev_map[hanzi]
    except Exception as e:
        return hanzi
