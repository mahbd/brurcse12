from django.urls import path
from . import views

app_name = 'jInfo'
urlpatterns = [
    path('', views.uri_info, name='home'),
    path('uri_points_update/', views.update_uri_points, name='update_uri_points'),
    path('uri_list/', views.uri_list, name='uri_list'),
    path('uri_list/e=<str:profile>', views.uri_list, name='url_ex'),
    path('cf_list/e=<str:handle>', views.cf_list, name='cfl_ex'),
    path('cf_list/', views.cf_list, name='cf_list'),
    path('cf_solve/', views.cf_solves, name='cf_solves'),
]
