from django.urls import path

from . import views

app_name = 'chat'
urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('send_message/', views.send_message, name='send'),
    path('<int:recipient_id>/', views.room, name='conversation'),
]
