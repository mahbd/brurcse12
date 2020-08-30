from django.contrib.auth.decorators import login_required
from home.all_functions import paging
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Topics, Tutorial, ContestName


def tutorials(request):
    topic_list = Topics.objects.filter(topic_name__isnull=False)
    topics, ids = {}, {}
    for topic in topic_list:
        topics[topic.topic_name] = Tutorial.objects.filter(topic_name_id=topic.id)[:10]
        ids[topic.topic_name] = topic.id

    context = {
        'title': "Tutorials",
        'topics': topics,
        'topic_list': topic_list,
        'ids': ids,
    }
    return render(request, 'tutorial/tutorials.html', context)


def sp_tutorial(request, topic_id):
    all_obj = Tutorial.objects.filter(topic_name_id=topic_id)
    tut_obj = paging(request, all_obj, 10)
    context = {
        'tut_obj': tut_obj,
        'title': Topics.objects.get(id=topic_id).topic_name,
        'topic_id': topic_id,
    }
    return render(request, 'tutorial/sp_tutorial.html', context)


@login_required
def add_tutorial(request, topic_id):
    if request.method == 'POST':
        topic = Topics.objects.get(id=topic_id)
        tut_title = request.POST['annTitle']
        tut_text = request.POST['annText']
        user_id = request.user.id
        new_tut = Tutorial(tut_title=tut_title, tut_text=tut_text, topic_name=topic, owner_id=user_id)
        new_tut.save()
        return redirect('tutorial:sp_tutorials', topic_id)
    context = {
        'title': Topics.objects.get(id=topic_id).topic_name,
        'topic_id': topic_id,
    }
    return render(request, 'tutorial/add_tutorial.html', context)


def tut(request, tut_id):
    tut_obj = Tutorial.objects.get(id=tut_id)
    if tut_obj.hidden and request.user.id != tut_obj.owner.id:
        if tut_obj.hidden_till > timezone.now():
            context = {
                'title': "Hidden",
                'wait_till': tut_obj.hidden_till
            }
            return render(request, 'tutorial/hidden.html', context)
        else:
            tut_obj.hidden = False
            tut_obj.save()
    context = {
        'title': tut_obj.tut_title,
        'tut_obj': tut_obj
    }
    return render(request, 'tutorial/tut.html', context)


@login_required
def edit_tutorial(request, tut_id):
    if request.user.id == Tutorial.objects.get(id=tut_id).owner.id or request.user.id == 1 or request.user.id == 2:
        if request.method == 'POST':
            tut_obj = Tutorial.objects.get(id=tut_id)
            if tut_obj.owner.id != request.user.id:
                raise Http404
            tut_obj.tut_title = request.POST['annTitle']
            tut_obj.tut_text = request.POST['annText']
            tut_obj.question_link = request.POST['annLink']
            tut_obj.save()
            return redirect('tutorial:tut', tut_id)
        tut_obj = Tutorial.objects.get(id=tut_id)
        context = {
            'tut_id': tut_id,
            'title': tut_obj.tut_title,
            'text': tut_obj.tut_text,
            'topic': tut_obj.topic_name,
            'annLink': tut_obj.question_link,
        }
        return render(request, 'tutorial/edit_tut.html', context)
    else:
        raise Http404


def contest_list(request):
    con_obj = ContestName.objects.all()
    context = {
        'title': "contest",
        'con_list': con_obj
    }
    return render(request, 'tutorial/contest_list.html', context)


def con_tut(request, con_id):
    con_obj = ContestName.objects.get(id=con_id)
    all_obj = Tutorial.objects.filter(contest_name=con_obj)
    tut_obj = paging(request, all_obj, 10)
    context = {
        'tut_obj': tut_obj,
        'title': ContestName.objects.get(id=con_id).contest_name,
        'topic_id': con_id,
    }
    return render(request, 'tutorial/contest_tutorial_list.html', context)


@login_required
def add_con_tut(request, con_id):
    if request.method == 'POST':
        contest = ContestName.objects.get(id=con_id)
        if contest.end < timezone.now():
            hidden = False
        else:
            hidden = True
        tut_title = request.POST['annTitle']
        tut_link = request.POST['annLink']
        tut_text = request.POST['annText']
        user_id = request.user.id
        new_tut = Tutorial(tut_title=tut_title, question_link=tut_link, tut_text=tut_text, contest_name=contest,
                           hidden=hidden, hidden_till=contest.end, owner_id=user_id)
        new_tut.save()
        return redirect('tutorial:contest', con_id)
    context = {
        'title': ContestName.objects.get(id=con_id).contest_name,
        'topic_id': con_id,
    }
    return render(request, 'tutorial/add_con_tut.html', context)
