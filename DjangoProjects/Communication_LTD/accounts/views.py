from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .forms import RegistrationForm, CustomPasswordChangeForm, CustomerForm, PasswordResetForm
import hashlib
import random
import string
from django.contrib import messages


def home_view(request):
    return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('password_reset_success')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            hashed_token = hashlib.sha1(token.encode()).hexdigest()
            send_mail(
                'Password Reset Request',
                f'Please use the following code to reset your password: {token}',
                'noreply@example.com',
                [email],
                fail_silently=False,
            )
            request.session['reset_token'] = hashed_token
            request.session['reset_user_id'] = user.id
            return redirect('reset_password')
    return render(request, 'forgot_password.html')


def reset_password_view(request):
    if request.method == 'POST':
        reset_code = request.POST.get('reset_code')
        new_password = request.POST.get('new_password')
        hashed_token = hashlib.sha1(reset_code.encode()).hexdigest()

        if hashed_token == request.session.get('reset_token'):
            user_id = request.session.get('reset_user_id')
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            del request.session['reset_token']
            del request.session['reset_user_id']
            return redirect('password_reset_success')
    return render(request, 'reset_password.html')


@login_required
def add_customer_view(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return render(request, 'customer_added.html', {'customer': customer})
    else:
        form = CustomerForm()
    return render(request, 'add_customer.html', {'form': form})
