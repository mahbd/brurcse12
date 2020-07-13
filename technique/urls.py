from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from technique import views

app_name = 'tech'
urlpatterns = [
    path('add_t/', views.add_technique, name='add_t'),
    path('view_t', views.view_technique, name='view_t'),
    path('add_problem_auto/', csrf_exempt(views.add_problem_auto), name='add_problem_auto'),
    path('cf_update/', views.cf_update, name='cf_update'),
    path('add_topic/', views.add_topic, name='add_topic'),
]