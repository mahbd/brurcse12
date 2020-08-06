from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from tutorial.models import Tutorial
from .models import Announce, AnnForm, Faq, DData


def index(request):
    ann_obj = Announce.objects.all()[:6]
    tut_obj = Tutorial.objects.all()[:6]
    pic_links = DData.objects.filter(type='home_gal')
    about_us = DData.objects.get(name="about_us")
    context = {
        'title': 'Home',
        'ann_obj': ann_obj,
        'tut_obj': tut_obj,
        'pic_links': pic_links,
        'about_us': about_us,
    }
    return render(request, 'home/home.html', context)


def faq(request):
    all_obj = Faq.objects.all().order_by('-date')
    spl_obj = Paginator(all_obj, 9)
    try:
        page_num = request.GET.get('page')
    except KeyError:
        page_num = 1
    faq_obj = spl_obj.get_page(page_num)
    context = {
        'title': "Faq",
        'ann_obj': faq_obj,
    }
    return render(request, 'home/faq.html', context)


def announcements(request):
    all_obj = Announce.objects.all().order_by('-date')
    spl_obj = Paginator(all_obj, 10)
    try:
        page_num = request.GET.get('page')
    except KeyError:
        page_num = 1
    ann_obj = spl_obj.get_page(page_num)
    context = {
        'title': "Announcement",
        'ann_obj': ann_obj,
    }
    return render(request, 'home/announcement.html', context)


@login_required
def add_edit_ann(request, ann_id=None):
    if ann_id:
        try:
            ann_obj = Announce.objects.get(id=ann_id)
        except Announce.DoesNotExist:
            return HttpResponse("Seems to be hacker")
        if ann_obj.owner != request.user:
            return HttpResponse("Seems to be hacker")
        title = 'Edit announcement'
    else:
        ann_obj = Announce()
        title = 'Add announcement'
    if request.method != 'POST':
        forms = AnnForm(instance=ann_obj)
    else:
        forms = AnnForm(instance=ann_obj, data=request.POST)
        if forms.is_valid():
            forms = forms.cleaned_data
            ann_obj.ann_title = forms['ann_title']
            ann_obj.ann_text = forms['ann_text']
            ann_obj.owner = request.user
            ann_obj.save()
            return redirect('home:announcement')
    context = {
        'title': title,
        'forms': forms,
        'ann_id': ann_id,
    }
    return render(request, 'home/add_announcement.html', context)


@login_required
def delete_ann(request, ann_id):
    obj = Announce.objects.get(id=ann_id)
    if obj.owner.id != request.user.id:
        raise Http404
    obj.delete()
    return redirect('home:announcement')
