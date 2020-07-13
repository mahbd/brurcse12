from message.models import LastMessage


def unread_check(request):
    unread = False
    last_messages_obj = LastMessage.objects.filter(recipient_id=request.user.id)
    for last_message in last_messages_obj:
        if not last_message.read:
            unread = True
    return {'unread': unread}
