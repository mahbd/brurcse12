import os
from datetime import datetime
from mysite.settings import BASE_DIR
import pytz
import requests
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render, redirect
from .models import ProbAnn
from home.models import SecretKeys

JAT = SecretKeys.objects.get(name='JAT').key

b_u_a = 'mahbd.pythonanywhere.com'


# b_u_a = '127.0.0.1:8000'


def problems(request):
    ann = ProbAnn.objects.all()
    data = {
        "JAT": JAT,
    }
    print("jat = " + JAT)
    problem_list = requests.post('http://' + b_u_a + '/compiler/get_problem_list/', data=data).json()
    if not problem_list['correct']:
        return HttpResponse(problem_list['status'])
    problem_list = problem_list['problems']
    for m in problem_list:
        print(m['problem_name'])
    context = {
        'title': 'problems',
        'ann': ann,
        'problem_list': problem_list,
        'contest_id': 0,
    }
    return render(request, 'problems/home.html', context)


def problem(request, problem_id):
    data = {
        "problem_id": problem_id,
        "JAT": JAT
    }
    problem_info = requests.post('http://' + b_u_a + '/compiler/get_problem/', data=data).json()
    print(problem_info)
    if not problem_info['correct']:
        return HttpResponse(problem_info['status'])
    problem_info = problem_info['problem']
    context = {
        'title': "problem",
        'problem': problem_info,
        'contest_id': 0,
    }
    return render(request, 'problems/problem.html', context)


def submission_result(request, problem_id):
    if request.method != 'POST':
        raise Http404
    try:
        submission_code = request.POST['code']
        contest_id = request.POST['contest_id']
    except KeyError:
        return HttpResponse("Bad input field")
    if request.user.is_authenticated:
        user_code = request.user.username
    else:
        user_code = 'guest'
    data = {
        "problem_id": problem_id,
        "submission_code": submission_code,
        "user_code": user_code,
        "language": "cpp",
        "contest_id": contest_id,
        "JAT": JAT,
    }
    res = requests.post('http://' + b_u_a + '/compiler/', data=data).json()
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
    data = {
        "JAT": JAT,
    }
    res = requests.post('http://' + b_u_a + '/compiler/get_contest_list/', data=data).json()
    if not res['correct']:
        return HttpResponse(res['status'])
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


@login_required
def add_problem(request, cid):
    if cid == 0:
        hidden = False
    else:
        hidden = True
    if request.method == 'POST':
        try:
            problem_name = request.POST['pn']
            problem_statement = request.POST['ps']
            input_terms = request.POST['it']
            output_terms = request.POST['ot']
            group = request.POST['group']
            correct_code = request.POST['cc']
        except KeyError:
            return HttpResponse("Error in forms")
        data = {
            "problem_name": problem_name,
            "problem_statement": problem_statement,
            "input_terms": input_terms,
            "output_terms": output_terms,
            "creator": request.user.username,
            "group": group,
            "correct_code": correct_code,
            "hidden": hidden,
            "JAT": JAT,
        }
        response = requests.post('http://' + b_u_a + '/compiler/add_problem/', data=data).json()
        print(response)
        if not response['correct']:
            return HttpResponse(response['status'])
        return redirect('problems:problem', response['id'])
    context = {
        'title': "add problem",
        'contest_id': cid,
    }
    return render(request, 'problems/add_problem.html', context)


def get_file(request, file_name):
    dir2 = os.path.join(BASE_DIR + '/home/static/' + file_name)
    file = open(dir2, 'r')
    res = ''
    for m in file:
        res += m.strip() + '\n'
    return HttpResponse(res, content_type='application/javascript')


def get_file_snippets(request, file_name):
    dir2 = os.path.join(BASE_DIR + '/home/static/snippets/' + file_name)
    file = open(dir2, 'r')
    res = ''
    for m in file:
        res += m.strip() + '\n'
    return HttpResponse(res, content_type='application/javascript')


def add_test_case(request, problem_id):
    if request.method == 'POST':
        data = {
            'problem_id': problem_id,
            'inputs': request.POST['inputs'],
            "JAT": JAT,
        }
        response = requests.post('http://' + b_u_a + '/compiler/add_test_case/', data=data).json()
        if not response['correct']:
            return HttpResponse(response['status'])
        context = {
            'result': response,
        }
        return render(request, 'problems/test_case_result.html', context)
    data = {
        "problem_id": problem_id,
        "JAT": JAT
    }
    code = requests.post('http://' + b_u_a + '/compiler/get_problem/', data=data).json()
    if not code['correct']:
        return HttpResponse(code['status'])
    code = code['problem']
    print(code)
    context = {
        'title': code['problem_name'],
        'problem_id': problem_id,
        'result': code,
    }
    return render(request, 'problems/add_test_case.html', context)


def contest_problems(request, contest_id):
    data = {
        'contest_id': contest_id,
        "JAT": JAT
    }
    problem_list = requests.post('http://' + b_u_a + '/compiler/get_contest_problems/', data=data).json()
    if not problem_list['correct']:
        return HttpResponse(problem_list['correct'])
    problem_list = problem_list['problems']
    for m in problem_list:
        print(m['problem_name'])
    context = {
        'title': 'problems',
        'ann': '',
        'problem_list': problem_list,
        'contest_id': contest_id,
    }
    return render(request, 'problems/home.html', context)


def contest_problem(request, problem_id, contest_id):
    data = {
        "problem_id": problem_id,
        "JAT": JAT,
    }
    problem_info = requests.post('http://' + b_u_a + '/compiler/get_problem/', data=data).json()
    print(problem_info)
    if not problem_info['correct']:
        return HttpResponse(problem_info['status'])
    problem_info = problem_info['problem']
    context = {
        'title': "problem",
        'problem': problem_info,
        'contest_id': contest_id,
    }
    return render(request, 'problems/problem.html', context)


def upcoming_contest(request):
    return HttpResponse("Coming soon....  Wait till then")

"""
def ended_contest(request):
    data = {
        'contest_id': 1,
        "JAT": JAT,
    }
    response = requests.post('http://127.0.0.1:8000/compiler/get_submissions_contest/', data=data).json()
    print(response)
    if not response['correct']:
        return HttpResponse(response['status'])
    submission_list = response['process']
    result = {}
    tz_dhaka = pytz.timezone('Asia/Dhaka')
    start_time = pytz.timezone('UTC').localize(datetime.strptime(cc['start_time'], "%Y-%m-%dT%H:%M:%SZ"))
    start_time = start_time.astimezone(tz_dhaka)
    for submission in submission_list:
        time = submission[0]
        time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        result[submission[1] + '_' + str(submission[2])] = time
    return HttpResponse("Contest Has ended.. Thank you for your help.")
"""
