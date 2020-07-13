import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect

from .models import Handle, Problems, Topic, Technique


@login_required
def add_technique(request):
    us = request.user
    if us.is_staff or us.first_name == '' or us.last_name == '' or us.email:
        if request.method == 'POST':
            Technique.objects.get_or_create(creator=request.user, text=request.POST['text'], code=request.POST['code'])
            tech = Technique.objects.get(creator=request.user, text=request.POST['text'], code=request.POST['code'])
            tech.topic.add(request.POST['TopicName'])
            tech.problems.add(request.POST['ProblemName'])
            return redirect('tech:view_t')
        problems = Problems.objects.all()
        topics = Topic.objects.all()
        problem_list, topic_list = [], []
        for problem in problems:
            problem_list.append(problem.id)
        for topic in topics:
            topic_list.append(topic.id)
        context = {
            'title': 'add technique',
            'problems': problems,
            'topics': topics,
            'topic_list': topic_list,
            'problem_list': problem_list,
        }
        return render(request, 'technique/add_t.html', context)
    else:
        return HttpResponse("Maybe you forgot to add First Name, Last Name, Email or you are Hacker")


def view_technique(request):
    res = requests.get('https://mah20.pythonanywhere.com/technique/get_t/').json()['res']
    context = {
        'title': 'view technique',
        'res': res
    }
    return render(request, 'technique/view_t.html', context)


def cf_update(request):
    handle_list = Handle.objects.all()
    for handle in handle_list:
        pre_submission = handle.last_submission
        add = True
        for p in range(1, 3):
            try_to_end = False
            url = 'https://codeforces.com/submissions/' + handle.handle + '/page/' + str(p)
            response = requests.get(url).content
            print(url)
            page = BeautifulSoup(response, 'html.parser')
            stat = page.findAll('tr')
            for m in stat:
                row = m.findAll('td', attrs={'class': 'status-cell status-small status-verdict-cell'})
                if len(row) != 0:
                    if str(row[0].text).strip() == 'Accepted':
                        submission = '99999999999999'
                        try:
                            submission = m.findAll('a', attrs={'class': 'view-source'})[0].text
                            if add:
                                handle.last_submission = submission
                                handle.save()
                                add = False
                        except IndexError:
                            pass
                        except AttributeError:
                            pass
                        print(submission)
                        if submission <= pre_submission:
                            try_to_end = True
                            break
                        td_link = m.findAll('td', attrs={'class': 'status-small'})[1]
                        name = str(m.findAll('td', attrs={'class': 'status-small'})[1].text).strip()[4:]
                        link = 'https://codeforces.com' + str(td_link.findAll('a')[0]['href'])
                        data = {
                            'name': name,
                            'link': link,
                            'solver': handle.handle
                        }
                        res_back = requests.post('http://mah20.pythonanywhere.com/cf/add_problem/', data=data).json()
                        print(res_back)
            if try_to_end:
                break
    return HttpResponse("Complete")


def add_problem_auto(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            link = request.POST['link']
            text = request.POST['text']
            solve = request.POST['solve']
            try:
                problem = Problems.objects.get(name=name, link=link, text=text)
                if problem.solve == solve:
                    return JsonResponse({'output': 'AlreadyAdded'})
                else:
                    problem.solve = solve
                    problem.save()
                    return JsonResponse({'output': 'updated'})
            except Problems.DoesNotExist:
                Problems.objects.create(name=name, link=link, text=text, solve=solve)
                return JsonResponse({'output': 'successful'})
        except KeyError:
            return JsonResponse({'status': False, 'reason': 'KeyError'})
    else:
        raise Http404


def add_topic(request):
    if request.method == 'POST':
        try:
            Topic.objects.get_or_create(name=request.POST['topic'])
            return redirect('tech:view_t')
        except KeyError:
            pass
    return render(request, 'technique/add_topic.html', {'title': 'add topic'})
