from django.shortcuts import render,redirect
from django.contrib import auth,messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserLoginForm,UserRegistrationForm,ProfileForm
from django.contrib.auth.decorators import login_required
from orders.models import Order,OrderItem
from django.db.models import Prefetch
def login(request):
    if request.method=='POST':
        form=UserLoginForm(data=request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=auth.authenticate(username=username,password=password)
            if user:
                auth.login(request,user)
                return HttpResponseRedirect(reverse('main:product_list'))
    else:
        form=UserLoginForm()
    return render(request,'users/login.html')

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            messages.success(request, f'{user.username}, Successful Registration')
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = UserRegistrationForm()
    return render(request, 'users/registration.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile was changed')
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)
    orders = Order.objects.filter(user=request.user).prefetch_related(Prefetch(
        'items',queryset=OrderItem.objects.select_related('product'),)).order_by('-id')

    return render(request, 'users/profile.html',{'form':form,'orders':orders})


def logout(request):
    auth.logout(request)
    return redirect(reverse('main:product_list'))

def google_auth(request):
    return render(request,'users/google_auth.html')

def google_login(request):
    return render(request,'users/googlelogin.html')

