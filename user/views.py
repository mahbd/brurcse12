from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from home.all_functions import email_validation, token_generator, get_name
from .models import UserInfo, Token
from django.contrib.auth.models import User
from mysite.settings import EMAIL_HOST_USER


def create_account(request):
    if request.method == 'POST':
        new_user = UserCreationForm(data=request.POST)
        if new_user.is_valid():
            new_user.save()
            return redirect('users:login')
    forms = UserCreationForm()
    context = {
        'title': 'Create Account',
        'forms': forms
    }
    return render(request, 'registration/register.html', context)


@login_required
def edit_info(request):
    if request.method == 'POST':
        email = request.POST['email']
        e_obj = email_validation(request.user, email)
        if not e_obj:
            context = {
                'title': 'already used',
                'class': 'alert-danger',
                'text': 'email is already used by someone. Please try another email.'
            }
            return render(request, 'registration/alert_page.html', context)
        elif e_obj.id != request.user.id:
            context = {
                'title': 'already used',
                'class': 'alert-danger',
                'text': e_obj.email + ' is already used by ' + get_name(e_obj) + ' . Please try another email.'
            }
            return render(request, 'registration/alert_page.html', context)
        else:
            user_obj = User.objects.get(id=request.user.id)
            try:
                inf_obj = UserInfo.objects.get(user=user_obj)
            except UserInfo.DoesNotExist:
                inf_obj = UserInfo(user=user_obj)
            user_obj.email = request.POST['email']
            user_obj.first_name = request.POST['first_name']
            user_obj.last_name = request.POST['last_name']
            inf_obj.blood_group = request.POST['blood_group']
            user_obj.save()
            inf_obj.save()
            return redirect('users:info')
    bg_options = ['NOT', 'A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    try:
        blood_group = UserInfo.objects.get(user_id=request.user.id)
    except UserInfo.DoesNotExist:
        blood_group = 'NOT'
    context = {
        'title': 'Edit info',
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'blood_group': blood_group,
        'bg_options': bg_options
    }
    return render(request, 'registration/edit_user_info.html', context)


def user_info(request):
    try:
        blood_group = UserInfo.objects.get(user_id=request.user.id).blood_group
    except UserInfo.DoesNotExist:
        blood_group = "Not Provided"
    context = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'blood_group': blood_group,
        'joined_on': request.user.date_joined,
        'last_visited': request.user.last_login
    }
    return render(request, 'registration/user_info.html', context)


def mailing(request):
    send_mail(
        'How are you',
        'It is long time we talked. Now asking, how are you?',
        'mahmuduly2000@gmail.com',
        ['mahmudula2000@gmail.com'],
        fail_silently=False
    )
    return HttpResponse("Success")


def test(request):
    return


def reset_pass_form(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            token = token_generator(10)
            new_tok = Token(token=token, type='pass_reset', identity=user.id)
            new_tok.save()
            message = "We are sorry that you forgot your password. But don't worry, you can change it now. click the " \
                      "link to reset brurcse12.herokuapp.com/user/reset_pass/" + token
            khk = send_mail(
                'Reset password',
                message,
                EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
            print(khk)
            context = {
                'title': 'success',
                'class': 'alert-success h3',
                'text': 'An email has sent to your email address. Please click and set you password.'
            }
            return render(request, 'registration/alert_page.html', context)
        except User.DoesNotExist:
            context = {
                'title': 'Failed',
                'class': 'alert-danger',
                'text': email + 'This is wrong email address. Please try again'
            }
            return render(request, 'registration/alert_page.html', context)
    context = {
        'title': 'email'
    }
    return render(request, 'registration/get_email.html', context)


def reset_pass(request, token):
    if request.method != 'POST':
        try:
            tok_obj = Token.objects.get(token=token)
        except Token.DoesNotExist:
            context = {
                'title': 'Failed',
                'class': 'alert-danger',
                'text': 'This link is wrong. Please try with another link'
            }
            return render(request, 'registration/alert_page.html', context)
        tok_obj.token = token_generator(15)
        tok_obj.save()
        forms = SetPasswordForm(User.objects.get(id=tok_obj.identity))
        context = {
            'title': 'set password',
            'forms': forms,
            'tok': tok_obj.token
        }
        return render(request, 'registration/reset_pass.html', context)
    try:
        tok_obj = Token.objects.get(token=token)
    except Token.DoesNotExist:
        context = {
            'title': 'Failed',
            'class': 'alert-danger',
            'text': 'Seems to be hacker. Password changes aborted'
        }
        return render(request, 'registration/alert_page.html', context)
    forms = SetPasswordForm(User.objects.get(id=tok_obj.identity), data=request.POST)
    if forms.is_valid():
        forms.save()
        context = {
            'title': 'Success',
            'class': 'alert-success',
            'text': 'Hurry!! Password change complete'
        }
        return render(request, 'registration/alert_page.html', context)
    context = {
        'title': 'Failed',
        'class': 'alert-danger',
        'text': 'Password form error'
    }
    return render(request, 'registration/alert_page.html', context)
