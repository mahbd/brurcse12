from django.urls import path

from problems import views
app_name = 'problems'
urlpatterns = [
    path('', views.problems, name='home'),

    path('problem=<int:problem_id>/', views.problem, name='problem'),
    path('sub_res=<int:problem_id>', views.submission_result, name='sub_res'),
    path('contest_list/', views.contest_list, name='contest_list'),
    path('add_problem=<int:cid>/', views.add_problem, name='add_problem'),
    path('get_file/<str:file_name>', views.get_file, name='get_file'),
    path('get_file/snippets/<str:file_name>', views.get_file_snippets, name='get_snippets'),
]
