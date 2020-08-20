from django.contrib import admin
from .models import Recipe, Image

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Image)