from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from food.models import Recipe, Image

# Create your views here.
def register(request):
  if request.method == "POST":
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('login')
  else:
    form = UserRegisterForm()
  return render(request, 'users/register.html', {'form':form})

@login_required(redirect_field_name='login')
def profile(request):

  if request.method == "POST":
    user_form = UserUpdateForm(request.POST, instance=request.user)
    profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

    if user_form.is_valid and profile_form.is_valid:
      user_form.save()
      profile_form.save()
      return redirect('home')

  else:
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance = request.user.profile)

  recipes = Recipe.objects.filter(author=request.user).order_by('-date_posted')
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
    'user_form': user_form,
    'profile_form': profile_form,
    'image_recipes': image_recipes,
  }

  return render(request, 'users/profile.html', context)
