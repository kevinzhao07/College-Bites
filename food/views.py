from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.forms import formset_factory 

from .models import Recipe, Image
from .forms import AddRecipeForm, AddImagesForm

# Create your views here.
@login_required(redirect_field_name='login')
def index(request):

  if request.method == "GET":
    filter_by = request.GET.get('filter_clean', False)
    filter_by_raw = request.GET.get('filter_raw', False)

    if filter_by_raw == False:
      filter_by_raw = "Date Created"

    if filter_by == False:
      filter_by = "-date_posted"

    recipes = Recipe.objects.order_by(filter_by)
    images = []

    for recipe in recipes:
      image = Image.objects.filter(recipe=recipe).first()
      default = Image.objects.filter(loopTime=100).first()

      if image is not None:
        images.append(image)

      else:
        images.append(default)

    image_recipes = zip(recipes, images)

    context = {
      "filter_by": filter_by_raw,
      "filter_by_clean": filter_by,
      "image_recipes": image_recipes,
    }

    return render(request, 'food/home.html', context)

  lastRecipe = Recipe.objects.order_by('-date_posted')
  lastImages = Image.objects.filter(recipe=lastRecipe).order_by('date_posted').first()
  lastRecipe.thumbnail = lastImages
  lastRecipe.save()

  print(lastRecipe)

  context = {
    "filter_by": "Date Created",
    "filter_by_clean": "-date_posted",
    "recipes": recipes,
  }
  return render(request, 'food/home.html', context)

@login_required(redirect_field_name='login')
def addrecipe(request):

  # we allow 3 images per recipe
  imagesFormSet = formset_factory(AddImagesForm, extra=3) 

  # if it is POST (submit button)
  if request.method == "POST":

    # get all the info from the formset
    formset = imagesFormSet(request.POST, request.FILES)
    if formset.is_valid(): # if it is valid

      # if there are images, find which recipe it belongs to (most recently created)
      loopTime = 0
      associated_recipe = Recipe.objects.all().order_by('-id').first()

      for form in formset.cleaned_data: # clean data
        image = form.get('image', False)

        if image: # if we get an image, then save it, save thumbnail

          new_image = Image(image=image, recipe=associated_recipe, loopTime=loopTime)
          new_image.save()

        loopTime = loopTime + 1

      return redirect('home') # return back home when we finish

  # if not POST, then simply give empty set
  else:
    formset = imagesFormSet()

  return render(request, 'food/addrecipe.html', {'formset':formset})

def add(request):
  user = request.user # must assume logged in
  if request.method == "GET":
    name = request.GET.get('name', '')
    link = request.GET.get('link', '')
    ingredients = request.GET.get('ingredients', '')
    recipe = request.GET.get('recipe', '')
    difficulty = request.GET.get('difficulty', 0)
    rating = request.GET.get('rating', 0)
    time = request.GET.get('time', 0)
    new_recipe = Recipe(name=name, link=link, ingredients=ingredients, recipe=recipe, difficulty=difficulty, rating=rating, author=user, cook_time=time)
    new_recipe.save()
    return HttpResponse('success')
  else:
    return HttpResponse('unsuccessful')

def updaterecipe(request, *args, **kwargs):
  if request.method == "GET":
    pk = request.GET.get('pk', '')
    recipe_object = get_object_or_404(Recipe, pk=pk)

    # things may have changed, get all.
    name = request.GET.get('name', '')
    link = request.GET.get('link', '')
    ingredients = request.GET.get('ingredients', '')
    recipe = request.GET.get('recipe', '')
    difficulty = request.GET.get('difficulty', 0)
    rating = request.GET.get('rating', 0)
    time = request.GET.get('time', 0)
    deleted = request.GET.get('deleted', '')

    recipe_object.name = name
    recipe_object.link = link
    recipe_object.ingredients = ingredients
    recipe_object.recipe = recipe
    recipe_object.difficulty = difficulty
    recipe_object.rating = rating
    recipe_object.time = time

    recipe_object.save()

    # if images have been deleted, delete them.
    loopCount = 0
    for value in deleted:
      if loopCount % 2 == 1:
        deleted_images = Image.objects.filter(recipe=recipe_object, loopTime=int(value)).first()
        deleted_images.delete()
      loopCount = loopCount + 1

    return HttpResponse('success')
  else:
    return HttpResponse('unsuccessful')

@login_required(redirect_field_name='login')
def detail(request, *args, **kwargs):
  recipe = get_object_or_404(Recipe, pk=kwargs['pk'])
  images = Image.objects.filter(recipe=recipe)

  context = {
    'recipe': recipe,
    'images': images,
  }

  return render(request, 'food/detail.html', context)

@login_required(redirect_field_name='login')
def update(request, *args, **kwargs):

  # delete old images associated with this recipe
  recipe = get_object_or_404(Recipe, pk=kwargs['pk'])
  images = Image.objects.filter(recipe=recipe)

  # we allow 3 images per recipe
  imagesFormSet = formset_factory(AddImagesForm, extra=3) 

  # if it is POST (submit button)
  if request.method == "POST":

    # get all the info from the formset
    formset = imagesFormSet(request.POST, request.FILES)
    if formset.is_valid(): # if it is valid

      # if there are images, find which recipe it belongs to (most recently created)
      loopTime = 0

      for form in formset.cleaned_data: # clean data
        image = form.get('image', False)

        if image: # if we get an image, then save it, save thumbnail
          new_image = Image(recipe=recipe, loopTime=loopTime, image=image)
          new_image.save()

          # if loopTime == 0:
          #   recipe.thumbnail = image
          #   recipe.save()

        loopTime = loopTime + 1

      return redirect('recipe-detail', pk=kwargs['pk']) # return back home when we finish

  # if not POST, then simply give empty set
  else:
    formset = imagesFormSet()

  context = {
    'recipe': recipe,
    'formset': formset,
    'images': images,
  }

  return render(request, 'food/editrecipe.html', context)