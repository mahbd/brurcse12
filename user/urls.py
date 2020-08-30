from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views


app_name = 'users'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.create_account, name='create'),
    path('edit/', csrf_exempt(views.edit_info), name='edit'),
    path('info/', views.user_info, name='info'),
    path('res_pass_form/', views.reset_pass_form, name='reset_pass_form'),
    path('reset_pass/<str:token>', views.reset_pass, name='reset_pass'),
    path('add_pic/', views.add_profile_image, name='add_pic'),
]
