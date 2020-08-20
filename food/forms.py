from django import forms
from .models import Recipe, Image

class AddRecipeForm(forms.ModelForm):
  class Meta:
    model = Recipe
    fields = ['name', 'ingredients', 'recipe']

class AddImagesForm(forms.ModelForm):
  class Meta:
    model = Image
    fields = ['image']