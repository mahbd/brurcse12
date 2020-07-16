from datetime import datetime

import pytz
import requests
from django.http import Http404, HttpResponse
from django.shortcuts import render
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
        user_code = request.user.username
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
    print(res)
    if not res['correct']:
        return HttpResponse(res['status'])
    else:
        context = {
            'title': 'result',
            'result': res,
            'code': submission_code,
        }
        return render(request, 'problems/sub_result.html', context)


def contest_list(request):
    res = requests.get('http://mahbd.pythonanywhere.com/compiler/get_contest_list/').json()
    upcoming_contests, running_contests, ended_contests = [], [], []
    res = res['contests']
    tz_dhaka = pytz.timezone('Asia/Dhaka')
    present = tz_dhaka.localize(datetime.now())
    for cc in res:
        start_time = pytz.timezone('UTC').localize(datetime.strptime(cc['start_time'], "%Y-%m-%dT%H:%M:%SZ"))
        end_time = pytz.timezone('UTC').localize(datetime.strptime(cc['end_time'], "%Y-%m-%dT%H:%M:%SZ"))
        start_time = start_time.astimezone(tz_dhaka)
        end_time = end_time.astimezone(tz_dhaka)
        cc['start_time'] = datetime.strftime(start_time, "%a %I:%M %P")
        cc['end_time'] = datetime.strftime(end_time, "%a %I:%M %P")
        if present < start_time:
            upcoming_contests.append(cc)
        elif end_time < present:
            ended_contests.append(cc)
        else:
            running_contests.append(cc)
    for contest in res:
        print(contest)
    context = {
        'title': 'contests',
        'running_contests': running_contests,
        'upcoming_contests': upcoming_contests,
        'ended_contest': ended_contests,
    }
    if len(running_contests) == 0:
        print("blank")
    return render(request, 'problems/contest_list.html', context)
