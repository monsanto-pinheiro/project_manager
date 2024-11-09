"""project_manager URL Configuration

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
from project_manager.views import LoginView, HomePageView, LogOutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('', HomePageView.as_view(), name='home'),
	path('dashboard/', HomePageView.as_view(), name='dashboard'),
	path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogOutView.as_view(), name='logout'),
    path('projects/', include('projects.urls')),
    path('pipelines/', include('pipelines.urls')),
    
    path('admin/', admin.site.urls),
]

if settings.DEBUG is True:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)