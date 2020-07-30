from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('tutorial/', include('tutorial.urls')),
    path('user/', include('user.urls')),
    path('chat/', include('chat.urls')),
    path('contests/', include('problems.urls')),
    path('jInfo/', include('judge_info.urls')),
    path('', include('home.urls')),
]
