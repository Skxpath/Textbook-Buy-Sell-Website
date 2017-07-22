from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ad, Textbook, AdForm, TextbookForm
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
def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    return render(request, 'textbook_app/ad_detail.html', {'ad': ad})

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
def ads_new(request):
    if request.method == 'POST':
        textbookForm = TextbookForm(request.POST)
        adForm = AdForm(request.POST)
        textbook_valid = textbookForm.is_valid()
        ad_valid = adForm.is_valid()
        # Do this because 'and' short circuits and we want to check both for validity
        if textbook_valid and ad_valid:
            textbook = textbookForm.save()
            ad = adForm.save(commit=False)
            ad.book = textbook
            ad.poster = request.user
            ad.save()
            return HttpResponseRedirect(reverse('textbook_app:ads'))
    else:
        textbookForm = TextbookForm()
        adForm = AdForm()
    return render(request, 'textbook_app/ads_new.html', {'textbookForm': textbookForm, 'adForm': adForm})

def textbook_edit(request, textbook_isbn):
    if request.method == "POST":
        textbook = get_object_or_404(Textbook, pk=textbook_isbn)
        textbook.title = request.POST['title']
        textbook.author = request.POST['author']
        textbook.description = request.POST['description']
        textbook.save()
        return HttpResponseRedirect(reverse('textbook_app:ads'))
    else:
        textbook = get_object_or_404(Textbook, pk=textbook_isbn)
        return render(request, "textbook_app/textbook_edit.html", {'textbook': textbook})
