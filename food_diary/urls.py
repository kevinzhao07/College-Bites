"""food_diary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from food import views as food_views
from users import views as users_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path('home/', food_views.index, name="home"),
    path('home/<int:pk>/', food_views.detail, name="recipe-detail"),
    path('home/update/<int:pk>/', food_views.update, name="recipe-update"),
    path('home/update/<int:pk>/updaterecipe/', food_views.updaterecipe, name="updaterecipe"),
    path('admin/', admin.site.urls),
    path('register/', users_views.register, name="register"),
    path('addrecipe/', include('food.urls')),
    path('profile/', users_views.profile, name="profile"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/login.html"), name="logout"),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)