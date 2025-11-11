from django import template

register = template.Library()

@register.filter
def chunk(list_data, chunk_size):
    """Divide una lista en chunks del tamaño especificado"""
    chunk_size = int(chunk_size)
    return [list_data[i:i + chunk_size] for i in range(0, len(list_data), chunk_size)]
