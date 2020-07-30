from operator import itemgetter

import requests
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

from user.models import UserInfo
from .models import UriInfo
from bs4 import BeautifulSoup as bs
import threading


def uri_point_update(info):
    url = info.profile_url
    response = requests.get(url).content
    page = bs(response, 'html.parser')
    stat = page.findAll('li')
    point, solved = False, False
    for m in stat:
        if m.text.find('Points:') != -1:
            point = m.text[8:].strip()
            print(point)
        if m.text.find('Solved:') != -1:
            solved = m.text[8:].strip()
            print(solved)
            break
    info.solves = int(solved)
    info.points = point
    info.save()


def uri_info(request):
    all_info = UriInfo.objects.all()
    context = {
        'title': 'Uri Judge Information',
        'all_info': all_info,
    }
    return render(request, 'judge_info/uri_and_home.html', context)


def update_uri_points(request):
    all_info = UriInfo.objects.all()
    for info in all_info:
        thread = threading.Thread(target=uri_point_update, args=[info])
        thread.start()
    return redirect('jInfo:home')


def cf_list(request):
    response = requests.get('https://judge-info.herokuapp.com/cf/get_list/').json()
    if not response["correct"]:
        return HttpResponse(response["status"])
    data = UserInfo.objects.exclude(handle='not_added')
    all_problem = response['data']
    paginator = Paginator(all_problem, 25)
    try:
        page_number = request.GET.get('page')
    except KeyError:
        page_number = 1
    all_problem = paginator.get_page(page_number)
    context = {
        "all_problem": all_problem,
        "title": "CF problem",
        "all_handle": data,
    }
    return render(request, 'judge_info/cf_problem.html', context)


def cf_solves(request):
    response = requests.get('https://judge-info.herokuapp.com/cf/total_solve/').json()
    if not response['correct']:
        return HttpResponse(response['status'])
    data = response['process']
    print(data)
    data.sort(key=itemgetter(1), reverse=True)
    context = {
        "title": "CF total solve",
        "all_person": data,
    }
    return render(request, 'judge_info/cf_solve.html', context)
