from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ttt/', include('technique.urls')),
    path('api/', include('api.urls')),
    path('tutorial/', include('tutorial.urls')),
    path('user/', include('user.urls')),
    path('message/', include('message.urls')),
    path('chat/', include('chat.urls')),
    path('problems/', include('problems.urls')),
    path('jInfo/', include('judge_info.urls')),
    path('', include('home.urls')),
]
