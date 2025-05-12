# your_app/templatetags/custom_filters.py

from django import template
import re
from django.utils.safestring import mark_safe

register = template.Library()

#  Custom Tampilan Penulisan Paragraf di Pengumuman
@register.filter
def urlize_blank(text):
    url_pattern = r'(https?://[^\s]+)'
    
    def replace_link(match):
        url = match.group(0)
        return f'<a href="{url}" target="_blank" class="text-green-600 underline">{url}</a>'
    
    result = re.sub(url_pattern, replace_link, text)
    return mark_safe(result.replace('\n', '<br>'))  # Biar enter jadi <br>

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def index(sequence, position):
    try:
        return sequence[int(position) - 1]  # Karena bulan dari 1-12, list dari 0
    except:
        return ''