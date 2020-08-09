from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import login, authenticate
from home.all_functions import token_generator
from .models import UserInfo, Token
from .forms import UserInfoForm, UploadFileForm
from django.contrib.auth.models import User
from mysite.settings import EMAIL_HOST_USER


def create_account(request):
    if request.method == 'POST':
        new_user = UserCreationForm(data=request.POST)
        if new_user.is_valid():
            new_user.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('users:info')
        else:
            context = {
                "title": "errors",
                "forms": new_user,
            }
            return render(request, 'registration/register.html', context)
    forms = UserCreationForm()
    context = {
        'title': 'Create Account',
        'forms': forms
    }
    return render(request, 'registration/register.html', context)


@login_required
def edit_info(request):
    if request.method == 'POST':
        forms = UserInfoForm(data=request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('users:info')
    form = UserInfoForm(instance=request.user.userinfo)
    context = {
        'title': 'Edit info',
        'forms': form
    }
    return render(request, 'registration/edit_user_info.html', context)


@login_required
def add_profile_image(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            user = UserInfo.objects.get(user=request.user)
            user.profile_image = request.FILES['file']
            user.save()
            return redirect('users:info')
    else:
        form = UploadFileForm()
    return render(request, 'registration/add_profile_picture.html', {'form': form})


@login_required
def user_info(request):
    UserInfo.objects.get_or_create(user_id=request.user.id)
    context = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'blood_group': request.user.userinfo.blood_group,
        'joined_on': request.user.date_joined,
        'last_visited': request.user.last_login,
        'cf_handle': request.user.userinfo.handle,
        'uri_id': request.user.userinfo.profile,
        'telegram_id': request.user.userinfo.telegram_id,
        'nick_name': request.user.userinfo.nick_name,
    }
    return render(request, 'registration/user_info.html', context)


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
            khk = send_mail('Reset password', message, EMAIL_HOST_USER, [user.email], fail_silently=False)
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
    # Send form to User
    if request.method != 'POST':
        # Token Problem
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
    # Password form Token problem
    try:
        tok_obj = Token.objects.get(token=token)
    except Token.DoesNotExist:
        context = {
            'title': 'Not allowed',
            'danger': 'Seems to be hacker. Password changes aborted'
        }
        return render(request, 'base/different_message.html', context)
    # Create form
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
