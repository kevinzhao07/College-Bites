from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
  
# Create your models here.

class Recipe(models.Model):
  name = models.CharField(max_length=100)
  link = models.CharField(max_length=280)
  ingredients = models.TextField()
  recipe = models.TextField()
  difficulty = models.IntegerField()
  rating = models.IntegerField()
  cook_time = models.IntegerField()
  date_posted = models.DateTimeField(default=timezone.now)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  thumbnail = models.ImageField(upload_to='recipe_images', default="default.jpg", null=True, blank=True)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('recipe-detail', kwargs={'pk': self.pk})

class Image(models.Model):
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, blank=True, null=True)
  image = models.ImageField(upload_to='recipe_images')
  loopTime = models.IntegerField()

  def __str__(self):
    if self.recipe:
      return f'Photo of {self.recipe.name}'

    else:
      return '**WARNING** DEFAULT PHOTO DO NOT DELETE **WARNING**'
