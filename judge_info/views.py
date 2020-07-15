import requests
from django.shortcuts import render, redirect
from .models import UriInfo
from bs4 import BeautifulSoup as bs


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
        info.solved = solved
        info.points = point
        info.save()
    return redirect('jInfo:home')