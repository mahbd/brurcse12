import os
from datetime import datetime, timezone
from operator import itemgetter

from django.core.paginator import Paginator

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


def time_convert(time):
    tz_dhaka = pytz.timezone('Asia/Dhaka')
    time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    time = pytz.timezone('UTC').localize(time)
    time = time.astimezone(tz_dhaka)
    return time


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


@login_required
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
    if request.method == 'POST':
        try:
            problem_name = request.POST['pn']
            problem_statement = request.POST['ps']
            input_terms = request.POST['it']
            output_terms = request.POST['ot']
            group = request.POST['group']
            correct_code = request.POST['cc']
            is_contest = request.POST['is_con']
            c_prob_id = request.POST['c_prob_id']
        except KeyError:
            return HttpResponse("Error in forms")
        if int(is_contest):
            hidden = True
        else:
            hidden = False
        data = {
            "problem_name": problem_name,
            "problem_statement": problem_statement,
            "input_terms": input_terms,
            "output_terms": output_terms,
            "creator": request.user.username,
            "group": group,
            "correct_code": correct_code,
            "hidden": hidden,
            "c_prob_id": c_prob_id,
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


@login_required
def add_test_case(request, problem_id):
    if not request.user.is_staff:
        return Http404
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
    context = {
        'title': "problem",
        'problem': problem_info,
        'contest_id': contest_id,
    }
    return render(request, 'problems/problem.html', context)


def upcoming_contest(request, contest_id):
    data = {
        'contest_id': contest_id,
        "JAT": JAT,
    }
    response = requests.post('http://' + b_u_a + '/compiler/get_contest_details/', data=data).json()
    if not response['correct']:
        return HttpResponse(response['status'])
    context = {
        "date": response['start_time'],
        "name": response['contest_name']
    }
    return render(request, 'problems/upcoming_contest.html', context)


def ended_contest(request, contest_id):
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
        "contest_id": -1,
        "f_c_id": contest_id,
        "problem_list": problem_list
    }
    return render(request, 'problems/home.html', context)


def standing(request, contest_id):
    data = {
        'contest_id': contest_id,
        "JAT": JAT,
    }
    response = requests.post('http://' + b_u_a + '/compiler/get_submissions_contest/', data=data).json()
    print(response)
    if not response['correct']:
        return HttpResponse(response['status'])
    submission_list = response['process']
    submission_list.reverse()
    info, time_calc, prob_calc = {}, {}, {}
    final_info = []
    for sub in submission_list:
        time = time_convert(sub[0])
        info[sub[1] + '___' + sub[2]] = (time - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds()
    for prob in info:
        time_calc[prob.split('___')[0]] = 0
        prob_calc[prob.split('___')[0]] = 0
    for prob in info:
        time_calc[prob.split('___')[0]] += info[prob]
        prob_calc[prob.split('___')[0]] += 1
    for per in time_calc:
        final_info.append([per, prob_calc[per], time_calc[per]])
    final_info.sort(key=itemgetter(2))
    final_info.sort(key=itemgetter(1), reverse=True)
    context = {
        'title': 'contest result',
        'results': final_info,
    }
    return render(request, 'problems/standing.html', context)


def all_submissions(request):
    data = {
        "JAT": JAT,
    }
    res = requests.post('http://' + b_u_a + '/compiler/all_submissions/', data=data).json()
    if not res['correct']:
        return HttpResponse(res['status'])
    sub_list = res['process']
    for sub in sub_list:
        time = time_convert(sub[0])
        sub[0] = datetime.strftime(time, "%D %I:%M %P")
    paginator = Paginator(sub_list, 25)
    try:
        page_number = request.GET.get('page')
    except KeyError:
        page_number = 1
    sub_list = paginator.get_page(page_number)
    context = {
        "title": "All submissions",
        "submission_list": sub_list,
    }
    return render(request, 'problems/all_submissions.html', context)


@login_required
def submission(request, sub_id):
    data = {
        "JAT": JAT,
        "submission_id": sub_id,
    }
    response = requests.post('http://' + b_u_a + '/compiler/get_submission/', data=data).json()
    if not response['correct']:
        return HttpResponse(response['status'])
    if response['restricted'] == 'submitter':
        if request.user.username != response['process']['submitter_code']:
            return HttpResponse('Contest is running or Internal error')
    time = time_convert(response['process']['date'])
    response['process']['date'] = datetime.strftime(time, "%D %I:%M %P")
    context = {
        "title": "submission",
        "submission": response['process']
    }
    return render(request, 'problems/submission.html', context)
