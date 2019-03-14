from django.urls import path, include
from . import views

app_name = 'aossie_scholar'

urlpatterns = [ path ('', views.IndexView.as_view(), name ='index'),
			]