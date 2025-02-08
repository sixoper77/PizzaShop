from django.shortcuts import render,redirect
from django.contrib import auth,messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserLoginForm,UserRegistrationForm,ProfileForm
from django.contrib.auth.decorators import login_required
from orders.models import Order,OrderItem

def login(request):
    if request.method=='POST':
        form=UserLoginForm(data=request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=auth.authenticate(username=username,password=password)
            if user:
                auth.login(request,user)
                return HttpResponseRedirect(reverse('main:product'))
    else:
        form=UserLoginForm()
    return render(request,'users/login.html')

def registration(request):
    if request.method=='POST':
        form=UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user=form.instance
            auth.login(request,user)
            messages.success(request,f'{user.username},Successful Registration')
    else:
        form=UserRegistrationForm()
    return render(request,'users/registration.html')
@login_required
def profile(request):
    return render(request,'users/profile.html')

def logout(request):
    ...

