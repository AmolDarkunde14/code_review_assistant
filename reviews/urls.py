from django.urls import path
from . import views


app_name = 'reviews'


urlpatterns = [
path('', views.upload_code, name='upload'),
path('report/<int:pk>/', views.view_report, name='view_report'),
]