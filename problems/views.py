import json
import os
from datetime import datetime, timezone
from operator import itemgetter
from random import randint

from django.contrib.auth.models import User
from django.core.paginator import Paginator

from home.all_functions import get_name
from mysite.settings import BASE_DIR
import pytz
import requests
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render, redirect

from user.models import UserDevice
from .models import ProbAnn
from home.models import SecretKeys, DData

#  Online Judge access key
JAT = SecretKeys.objects.get(name='JAT').key

# Base Link address
b_u_a = 'mahbd.pythonanywhere.com'


# b_u_a = '127.0.0.1:8001'


def record_device(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'guest'
    UserDevice.objects.get_or_create(username=username,
                                     device=request.META.get('HTTP_USER_AGENT', ''))
    user_obj = UserDevice.objects.get(username=username,
                                      device=request.META.get('HTTP_USER_AGENT', ''))
    user_obj.time = datetime.now()
    user_obj.save()
    print(user_obj.device)


# Convert UTC string to python Dhaka timezone
def time_convert(time):
    tz_dhaka = pytz.timezone('Asia/Dhaka')
    time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    time = pytz.timezone('UTC').localize(time)
    time = time.astimezone(tz_dhaka)
    return time


# Editor file fetching
def get_file(request, file_name):
    if file_name == "mode-c_cpp.js":
        file = requests.get('https://drive.google.com/uc?export=download&id=1pm1g-mt3BJstjKlUYAEyETuW6pVH4v6Q').content
    elif file_name == "theme-chrome.js":
        file = requests.get('https://drive.google.com/uc?export=download&id=1Wi77PRnsw3cVEc9s4WX2l9W_GwHTjqVM').content
    else:
        file = requests.get('https://drive.google.com/uc?export=download&id=1qh6kmc7XVi06_6tEeRWdGzvzCFycapop').content
    return HttpResponse(file, content_type='application/javascript')


def get_file_snippets(request, file_name):
    dir2 = os.path.join(BASE_DIR + '/home/static/snippets/' + file_name)
    file = open(dir2, 'r')
    res = ''
    for m in file:
        res += m.strip() + '\n'
    return HttpResponse(res, content_type='application/javascript')


# Problem Section
def problems(request):  # All visible problem list
    record_device(request)
    ann = ProbAnn.objects.all()
    data = {
        "JAT": JAT,
    }
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


@login_required
def problem(request, problem_id, contest_id=0):  # Single problem
    record_device(request)
    data = {
        "problem_id": problem_id,
        "JAT": JAT
    }
    problem_info = requests.post('http://' + b_u_a + '/compiler/get_problem/', data=data).json()
    if not problem_info['correct']:
        return HttpResponse(problem_info["status"])
    if problem_info["restricted"] == "submitter":
        if request.user.is_staff:
            pass
        elif request.user.username != problem_info["problem"]["creator"]:
            context = {
                'title': 'not allowed',
                'danger': 'Sorry!! You are not allowed to view this'
            }
            return render(request, 'base/different_message.html', context)
    problem_info = problem_info['problem']
    context = {
        'title': "problem",
        'problem': problem_info,
        'contest_id': contest_id,
    }
    return render(request, 'problems/problem.html', context)


@login_required
def add_problem(request, cid):  # Add problem for both contest and regular
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
            "cid": cid
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


# Contest section
def contest_list(request):
    record_device(request)
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
        cc['creator_nick'] = cc['creator']
        try:
            cc['creator_nick'] = User.objects.get(username=cc['creator']).userinfo.nick_name
        except User.DoesNotExist:
            pass
        try:
            cc['tester'] = User.objects.get(username=cc['tester']).userinfo.nick_name
        except User.DoesNotExist:
            pass
        cc['start_time'] = datetime.strftime(start_time, "%d %b %y::%I:%M %P")
        cc['end_time'] = datetime.strftime(end_time, "%d %b %y::%I:%M %P")
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


def contest_problems(request, contest_id):
    record_device(request)
    data = {
        'contest_id': contest_id,
        "JAT": JAT
    }
    problem_list = requests.post('http://' + b_u_a + '/compiler/get_contest_problems/', data=data).json()
    if not problem_list['correct']:
        return HttpResponse(problem_list['correct'])
    if problem_list['restricted'] == 'submitter':
        if not request.user.is_superuser and not request.user.username == problem_list['creator']:
            return redirect('problems:upcoming_contest', contest_id)
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
        "name": response['contest_name'],
        "contest_id": contest_id,
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
    if problem_list['restricted'] == 'submitter':
        return redirect('problems:upcoming_contest', contest_id)
    problem_list = problem_list['problems']
    for m in problem_list:
        print(m['problem_name'])
    context = {
        "contest_id": -1,
        "f_c_id": contest_id,
        "problem_list": problem_list
    }
    return render(request, 'problems/home.html', context)


def standing(request, contest_id=False):
    record_device(request)
    if not contest_id:
        contest_id = DData.objects.get(name='current_standing').data
    data = {
        'contest_id': contest_id,
        "JAT": JAT,
    }
    response = requests.post('http://' + b_u_a + '/compiler/get_contest_details/', data=data).json()
    contest_name = response['contest_name']
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
        'contest_name': contest_name,
        'results': final_info,
    }
    return render(request, 'problems/standing.html', context)


# Submission section
def all_submissions(request):
    record_device(request)
    data = {
        "JAT": JAT,
    }
    res = requests.post('http://' + b_u_a + '/compiler/all_submissions/', data=data).json()
    if not res['correct']:
        return HttpResponse(res['status'])
    sub_list = res['process']
    for sub in sub_list:
        try:
            nick_name = User.objects.get(username=sub[1]).userinfo.nick_name
            if nick_name != 'not_added':
                sub[1] = nick_name
        except:
            pass
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
    record_device(request)
    data = {
        "JAT": JAT,
        "submission_id": sub_id,
    }
    response = requests.post('http://' + b_u_a + '/compiler/get_submission/', data=data).json()
    if not response['correct']:
        return HttpResponse(response['status'])
    if response['restricted'] == 'submitter':
        if request.user.is_superuser or response["process"]["problem_creator"] == request.user.username:
            pass
        elif request.user.username != response['process']['submitter_code']:
            context = {
                "info": "Contest is running. Please try this after contest"
            }
            return render(request, 'base/different_message.html', context)
    time = time_convert(response['process']['date'])
    response['process']['date'] = datetime.strftime(time, "%D %I:%M %P")
    context = {
        "title": "submission",
        "submission": response['process']
    }
    return render(request, 'problems/submission.html', context)


@login_required
def submission_result(request, problem_id):
    if request.method != 'POST':
        raise Http404
    try:
        submission_code = request.POST['code']
        contest_id = request.POST['contest_id']
    except KeyError:
        return HttpResponse("Bad input field")
    data = {
        'contest_id': int(contest_id),
        "JAT": JAT,
    }
    response = requests.post('http://' + b_u_a + '/compiler/get_contest_details/', data=data).json()
    if request.user.is_superuser:
        is_test = True
    elif response["correct"] == request.user.username:
        if response['creator'] == request.user.username:
            is_test = True
    else:
        is_test = False
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
        "is_test": is_test,
        "JAT": JAT,
    }
    res = requests.post('http://' + b_u_a + '/compiler/', data=data).json()
    print(res)
    if not res['correct']:
        return HttpResponse(res['status'])
    try:
        message = "Hey " + get_name(request.user) + ",\nYour code's result for >>" + res['problem_name'] + "<< is " + \
                  res['verdict'] + ". Thanks for participating"
        data = {
            "message": message,
            "chat_id": request.user.userinfo.telegram_id
        }
        kkk = requests.post('http://pb12.herokuapp.com/bot/send_tm/', data=data).content
        print(kkk)
    except:
        pass
    context = {
        'title': 'result',
        'result': res,
        'code': submission_code,
    }
    return render(request, 'problems/sub_result.html', context)


# Test case section
def test_case_list(request, problem_id):
    data = {
        "problem_id": problem_id,
        "JAT": JAT
    }
    response = requests.post('http://' + b_u_a + '/compiler/get_ptc/', data=data).json()
    if not response['correct']:
        return HttpResponse(response['status'])
    context = {
        "title": "test case list",
        "test_list": response['process']
    }
    return render(request, 'problems/test_case_list.html', context)


@login_required
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


def add_test_case_api(request, problem_id):
    if request.method == 'POST':
        data = {
            'problem_id': problem_id,
            'inputs': json.loads(request.body)['inputs'],
            "JAT": JAT,
        }
        response = requests.post('http://' + b_u_a + '/compiler/add_test_case/', data=data).json()
        if not response['correct']:
            return JsonResponse(response['status'], safe=False)
        return JsonResponse(response['process'][1], safe=False)
    return JsonResponse({"status": "Couldn't process"})
