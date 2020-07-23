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
    path('contest_problems=<int:contest_id>/', views.contest_problems, name='contest_problem'),
    path('add_test_case=<int:problem_id>/', views.add_test_case, name='add_test_case'),
    path('contest_problem=<int:problem_id>cid=<int:contest_id>/', views.contest_problem, name='s_c_problem'),
    path('upcoming_contest/', views.upcoming_contest, name='upcoming_contest'),
    path('ended_contest<int:contest_id>/', views.ended_contest, name='ended_contest'),
    path('all_submissions/', views.all_submissions, name='all_submissions'),
    path('submission=<int:sub_id>/', views.submission, name='submission'),
    path('standing=<int:contest_id>/', views.standing, name='standing'),
]
