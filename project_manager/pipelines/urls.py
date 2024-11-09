'''
Created on 17/03/2020

@author: mmp
'''
from django.urls import path
from pipelines import views

## same, url is going to be
# url(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive)
# path('articles/<int:year>/', views.year_archive)

urlpatterns = [
		path('pipelines/', views.PipelinesView.as_view(), name='pipelines'),
		path('pipelines_add/', views.PipelinesView.as_view(), name='pipeline-add'),
		path('pipelines_update/<int:pk>', views.PipelinesView.as_view(), name='pipeline-update'),
		
]




