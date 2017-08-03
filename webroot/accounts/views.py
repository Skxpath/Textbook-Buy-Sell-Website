from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            # Return server-side errors to the user via the form object.
            return render(request, 'accounts/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')
