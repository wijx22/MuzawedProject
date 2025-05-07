# templatetags/custom_tags.py
from django import template
from products.models import CategoryImage  
from django.templatetags.static import static

register = template.Library()

@register.simple_tag
def get_category_image(category_name):
    try:
        category_image = CategoryImage.objects.get(category_name=category_name)
        return category_image.image.url if category_image.image else static('image/default.png')  # Return image URL or default
    except CategoryImage.DoesNotExist:
        return static('image/default.png')  # Return default if no image found