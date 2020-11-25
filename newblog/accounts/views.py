from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import (UserSignupForm, UserLoginForm)
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from newblog.articles.models import Article
from django.contrib.auth.decorators import login_required

def sign_in(request):
    return render(request, 'accounts/sign-in.html',)
# Create your views here.


def login_view(request):
    next_location = request.POST.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        elif User.objects.filter(email=username).exists():
            get_username = User.objects.get(email=username).username
            user = authenticate(request, username=get_username, password=password)
        if user is not None:
            login(request, user)
        if next_location:
            return redirect(next_location)
        else:
            return HttpResponseRedirect('/news/')
    context = {
        'form': form
    }
    return render(request, 'registration/login.html', context)


def register_view(request):
    hide_value = 'yes'
    next_location = request.POST.get('next')
    form = UserSignupForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=user.password)
        login(request, new_user)
        if next_location:
            return redirect(next_location)
        return redirect('index/')
    context = {
        'form': form,
        'hide': hide_value
    }
    return render(request, 'registration/signup.html', context)


@login_required
def logoutview(request):
    next = request.POST.get('next')
    if request.user.is_authenticated():
        logout(request, request.user)
    if next:
        return redirect('index/')
    return redirect('index/')
