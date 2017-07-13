from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def ads_list(request):
    return render(request, 'textbook_app/ads_list.html')
