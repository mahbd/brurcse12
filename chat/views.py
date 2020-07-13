from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import models
from django.http import HttpResponse
from django.shortcuts import render

from message.models import Message, LastMessage
from home.all_functions import make_read, last_message_update, get_name
from user.views import token_generator


def index(request):
    return render(request, 'chat/index.html')


def conversation_view(request, room_name):
    context = {
        'room_name': room_name
    }
    return render(request, 'chat/room.html', context)


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
