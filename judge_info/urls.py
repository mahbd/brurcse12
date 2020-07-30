from django.urls import path
from . import views

app_name = 'jInfo'
urlpatterns = [
    path('', views.uri_info, name='home'),
    path('uri_points_update/', views.update_uri_points, name='update_uri_points'),
    path('cf_list/', views.cf_list, name='cf_list'),
    path('cf_solve/', views.cf_solves, name='cf_solves'),
]
