from django import template

register = template.Library()

@register.filter
def add_thousands_separator(value):
    """
    Añade separadores de miles al valor numérico y lo muestra como un número entero.
    """
    try:
        # Convertir el valor a entero para eliminar decimales
        value = int(float(value))  # Asegura que también funcione con strings o floats
        # Formatear con separadores de miles
        return f"{value:,}".replace(",", ".")
    except (ValueError, TypeError):
        return value
