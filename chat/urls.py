from django.urls import path

from . import views
app_name = 'chat'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:recipient_id>/', views.room, name='room'),
    path('pv/<str:room_name>/', views.conversation_view, name='conversation'),
]
