from django.urls import path

from problems import views
app_name = 'problems'
urlpatterns = [
    path('', views.problems, name='home'),
    path('problem=<int:problem_id>/', views.problem, name='problem'),
    path('sub_res=<int:problem_id>', views.submission_result, name='sub_res'),
    path('contest_list/', views.contest_list, name='contest_list'),
]
