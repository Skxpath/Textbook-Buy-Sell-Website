from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Ad, Textbook
from django.urls import reverse
from django.http import HttpResponseRedirect


def ads_list(request):
    ads_list = Ad.objects.all()
    context = {
        # Note: the user may not be present here since login isn't required for this page
        'user': request.user,
        'ads_list': ads_list
    }
    return render(request, 'textbook_app/ads_list.html', context)

@login_required
def profile(request):
    user_ads = Ad.objects.filter(poster=request.user.id)
    context = {
        'user': request.user,
        'ads_list': user_ads,
    }
    return render(request, 'textbook_app/profile.html', context)

# Note: these are VERY rough versions of the 'new ad' views
# Once implemented properly, the user should be able to search through existing textbooks
# and link that textbook to their ad if a textbook already exists. Otherwise, they can add a new one
@login_required
def ads_new_page(request):
    return render(request, 'textbook_app/ads_new.html')

@login_required
def ads_new_request(request):
    textbook = Textbook(
        title = request.POST['title'],
        author = request.POST['author'],
        description = request.POST['description'],
        isbn = request.POST['isbn'],
    )
    textbook.save()
    ad = Ad(
        # TODO: don't hardcode values here!
        price = 3.50,
        condition = 'GOOD',
        book = textbook,
        poster = request.user,
    )
    ad.save()
    return HttpResponseRedirect(reverse('textbook_app:ads'))
