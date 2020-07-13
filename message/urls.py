from django.urls import path
from chat.views import room
from . import views

app_name = 'message'
urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('send_message/', views.send_message, name='send'),
    path('pv/<int:recipient_id>', room, name='conversation'),
    path('tm/<int:recipient_id>', views.target_message, name='target'),
    path('group_message/', views.group, name='group'),
    path('gv/<int:group_id>', views.group_view, name='group_view'),
]
