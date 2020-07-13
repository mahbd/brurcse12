from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('', views.api, name='api'),
    path('dis=<str:name>/', views.district, name='district'),
    path('cnt=<str:name>/', views.country, name='country'),
    path('dhaka=<str:name>', views.dhaka, name='dhaka'),
    path('force_update/', views.force_update, name='update'),
    path('world/', views.world, name='world'),
]
