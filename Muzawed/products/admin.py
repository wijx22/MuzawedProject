from django.contrib import admin

# Register your models here.

from .models import Product,CategoryImage

admin.site.register(Product)

admin.site.register(CategoryImage)
