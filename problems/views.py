import requests
from django.http import Http404, HttpResponse
from django.shortcuts import render

from home.all_functions import token_generator
from user.models import UserInfo
from .models import ProbAnn


def problems(request):
    ann = ProbAnn.objects.all()
    problem_list = requests.get('http://mahbd.pythonanywhere.com/compiler/get_problem_list/').json()['problems']
    for m in problem_list:
        print(m['problem_name'])
    context = {
        'title': 'problems',
        'ann': ann,
        'problem_list': problem_list,
    }
    return render(request, 'problems/home.html', context)


def problem(request, problem_id):
    problem_info = requests.get('http://mahbd.pythonanywhere.com/compiler/get_problem=' + str(problem_id)).json()
    context = {
        'title': "problem",
        'problem': problem_info,
    }
    return render(request, 'problems/problem.html', context)


def submission_result(request, problem_id):
    if request.method != 'POST':
        raise Http404
    submission_code = request.POST['code']
    if request.user.is_authenticated:
        user_code = UserInfo.objects.get(user_id=request.user.id).user_code
        if user_code == 'not_added':
            user_code = token_generator(10)
            user = UserInfo.objects.get(user_id=request.user.id)
            user.user_code = user_code
            user.save()
    else:
        user_code = 'guest'
    data = {
        "problem_id": problem_id,
        "submission_code": submission_code,
        "user_code": user_code,
        "language": "cpp",
        "contest_id": 0,
    }
    res = requests.post('http://mahbd.pythonanywhere.com/compiler/', data=data).json()
    if not res['correct']:
        return HttpResponse(res['status'])
    else:
        context = {
            'title': 'result',
            'result': res,
            'code': submission_code,
        }
        return render(request, 'problems/sub_result.html', context)

