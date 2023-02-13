"""mehak_coffe_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('api/', include("model.urls")),
    path("i18n/", include("django.conf.urls.i18n"))
]


urlpatterns += i18n_patterns(path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'))
urlpatterns += i18n_patterns(path("", admin.site.urls))
