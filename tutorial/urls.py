from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'tutorial'
urlpatterns = [
    path('', views.tutorials, name='tutorials'),
    path('s/<int:topic_id>/', views.sp_tutorial, name='sp_tutorials'),
    path('add/<int:topic_id>', csrf_exempt(views.add_tutorial), name='add_tut'),
    path('tut/<int:tut_id>', views.tut, name='tut'),
    path('edit/<int:tut_id>', csrf_exempt(views.edit_tutorial), name='edit'),
    path('contest/', views.contest_list, name='contest_list'),
    path('contest/sn/<int:con_id>', views.con_tut, name='contest'),
    path('con/an/<int:con_id>', csrf_exempt(views.add_con_tut), name='add_con_tut'),
]
