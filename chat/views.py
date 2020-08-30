from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import models
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Message, LastMessage
from home.all_functions import make_read, last_message_update, get_name, token_generator


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
    return render(request, 'chat/message.html', context)


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
                return redirect('chat:inbox')
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
    return render(request, 'chat/send_message.html', context)


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
    return render(request, 'chat/target_message.html', context)


def room(request, recipient_id):
    make_read(request)
    if request.method == 'POST':
        message = request.POST['message']
        last_message_update(request, recipient_id, message)
        new_obj = Message(message=message, sender=request.user, recipient_id=recipient_id)
        new_obj.save()
    message_list_query = Message.objects.filter(((models.Q(sender_id=request.user.id) & models.Q(
        recipient_id=recipient_id)) | (models.Q(sender_id=recipient_id) & models.Q(recipient_id=request.user.id))))
    message_page_all = Paginator(message_list_query, 10)
    try:
        page_num = request.GET.get('page')
    except KeyError:
        page_num = 1
    message_page = message_page_all.get_page(page_num)
    recipient_name = get_name(User.objects.get(id=recipient_id))
    last_message_obj = LastMessage.objects.filter(((models.Q(sender_id=request.user.id) &
                                                    models.Q(recipient_id=recipient_id)) |
                                                   (models.Q(sender_id=recipient_id) &
                                                    models.Q(recipient_id=request.user.id))))
    try:
        room_name = last_message_obj[0].room_name
    except IndexError:
        raise HttpResponse("Please send a message using send button. Then come here")
    try:
        if len(room_name) < 4:
            room_name = token_generator(10)
            message_id_1 = last_message_obj[0].id
            obj = LastMessage.objects.get(id=message_id_1)
            obj.room_name = room_name
            obj.save()
    except TypeError:
        room_name = token_generator(10)
        message_id_1 = last_message_obj[0].id
        obj = LastMessage.objects.get(id=message_id_1)
        obj.room_name = room_name
        obj.save()
    context = {
        'title': recipient_name,
        'message_list_obj': message_page,
        'recipient_id': recipient_id,
        'ann_obj': message_page,
        'room_name': room_name
    }
    return render(request, 'chat/room.html', context)
