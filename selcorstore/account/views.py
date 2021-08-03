from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


# View created for user login with authentication
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Logowanie zakończyło się sukcesem.")
                else:
                    return HttpResponse("Konto jest zablokowane.")
            else:
                return HttpResponse("Nieprawidłowe dane logowania.")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


# View created for logged user
@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})