import json
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import models
from django.http import HttpResponse
from django.shortcuts import render, redirect
from home.all_functions import make_read, get_name, last_message_update
from .models import Message, LastMessage, GroupInfo


@login_required
def inbox(request):
    make_read(request)
    message_list_query = LastMessage.objects.filter(
        (models.Q(recipient_id=request.user.id) | models.Q(sender_id=request.user.id)))
    message_page_all = Paginator(message_list_query, 10)
    try:
        page_num = request.GET.get('page')
    except KeyError:
        page_num = 1
    message_page = message_page_all.get_page(page_num)
    message_list = {}
    sender_ids = {}
    for message in message_page:
        if message.sender.id == request.user.id:
            message_list[get_name(User.objects.get(id=message.recipient_id))] = message.message
            sender_ids[get_name(User.objects.get(id=message.recipient_id))] = message.recipient_id
        else:
            message_list[get_name(message.sender)] = message.message
            sender_ids[get_name(message.sender)] = message.sender.id
    context = {
        'title': 'Inbox',
        'message_list': message_list,
        'sender_ids': sender_ids,
        'ann_obj': message_page
    }
    return render(request, 'message/message.html', context)


@login_required
def send_message(request):
    if request.method == 'POST':
        try:
            recipient = User.objects.get(username=request.POST['username'])
            message = request.POST['message']
            if message != '':
                new_obj = Message(message=request.POST['message'], sender=request.user, recipient_id=recipient.id)
                last_message_update(request.user, recipient.id, message)
                new_obj.save()
                return redirect('message:inbox')
        except User.DoesNotExist:
            pass
    user_list = []
    user_obj = User.objects.all()
    for user in user_obj:
        user_list.append(user.username)
    context = {
        'title': 'send message',
        'user_info': user_obj,
        'user_list': user_list
    }
    return render(request, 'message/send_message.html', context)


@login_required
def target_message(request, recipient_id):
    if request.method == 'POST':
        message = request.POST['message']
        if message != '':
            last_message_update(request.user, recipient_id, message)
            new_obj = Message(sender=request.user, recipient_id=recipient_id, message=message)
            new_obj.save()
            return redirect('message:conversation', recipient_id)
    recipient_name = get_name(User.objects.get(id=recipient_id))
    context = {
        'title': recipient_name,
        'recipient_id': recipient_id
    }
    return render(request, 'message/target_message.html', context)


def bot_get(request):
    data = json.loads(request.body)
    print(data)
    try:
        chat_type = data['message']['chat']['chat_type']
    except KeyError:
        return HttpResponse("Success")
    if chat_type == 'group':
        try:
            message = data['message']['text']
        except KeyError:
            message = "A file shared"
        try:
            fn = data['message']['from']['first_name']
        except KeyError:
            fn = "Unknown"
        try:
            ln = data['message']['from']['last_name']
        except KeyError:
            ln = "Unknown"
        sender = fn + ' ' + ln
        group_name = data['message']['chat']['title']
        GroupInfo.objects.get_or_create(name=group_name)
        group_obj = GroupInfo.objects.get(name=group_name)
        group_id = group_obj.id
        new_mes = Message(group_id=group_id, message=message, telegram_sender=sender)
        try:
            las_mes = LastMessage.objects.get(group_id=group_id)
            las_mes.message = message
        except LastMessage.DoesNotExist:
            las_mes = LastMessage(group_id=group_id, message=message)
        new_mes.save()
        las_mes.save()
        return HttpResponse("Success")
    elif chat_type == 'private':
        telegram_url = "https://api.telegram.org/bot"
        tutorial_bot_token = "1214433734:AAGgKkYrFuiMSXmRNoUmVPvaBUD9HVVgVuM"
        message = data['message']['text']
        chat_id = data['message']['chat']['id']
        sender = data['message']['from']['first_name'] + " " + data['message']['from']['last_name']
        print(sender)
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        requests.post(
            f"{telegram_url}{tutorial_bot_token}/sendMessage", data=data
        )
        return HttpResponse("Success")
    else:
        return HttpResponse("Success")


def group(request):
    group_list_query = User.objects.get(id=request.user.id).groupinfo_set.all()
    group_list = {}
    for group_obj in group_list_query:
        try:
            group_list[group_obj.name] = LastMessage.objects.get(group_id=group_obj.id)
        except LastMessage.DoesNotExist:
            pass
    context = {
        'title': 'group',
        'group_list': group_list
    }
    return render(request, 'message/group.html', context)


def group_view(request, group_id):
    group_obj = GroupInfo.objects.get(id=group_id)
    all_message = Message.objects.filter(group_id=group_id)
    message_page_all = Paginator(all_message, 10)
    try:
        page_num = request.GET.get('page')
    except KeyError:
        page_num = 1
    message_page = message_page_all.get_page(page_num)
    context = {
        'title': group_obj.name,
        'all_message': message_page,
        'ann_obj': message_page
    }
    return render(request, 'message/group_view.html', context)
