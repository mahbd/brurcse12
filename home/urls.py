from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from message.views import bot_get

app_name = "home"
urlpatterns = [
    path('', views.index, name="home"),
    path('faq/', views.faq, name='faq'),
    path('bot/', csrf_exempt(bot_get), name='bot_get'),
    path('ann/', views.announcements, name="announcement"),
    path('add/', csrf_exempt(views.add_edit_ann), name='add_ann'),
    path('edit/<int:ann_id>', views.add_edit_ann, name='edit_ann'),
    path('delete/<int:ann_id>', views.delete_ann, name='delete_ann'),
]
