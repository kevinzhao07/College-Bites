from . import views as food_views
from django.urls import path

urlpatterns = [
  path('add/', food_views.add, name="add"),
  path('', food_views.addrecipe, name="addrecipe"),
]