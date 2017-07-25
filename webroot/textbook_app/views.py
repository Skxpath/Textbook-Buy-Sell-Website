from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from .models import Ad, Textbook, AdForm, TextbookForm
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

NUM_ADS_PER_PAGE = 2

def ads_list(request):
    context = {
        # Note: the user may not be present here since login isn't required for this page
        'user': request.user,
    }
    return render(request, 'textbook_app/ads_list.html', context)

def ads_search(request):
    ads_all = Ad.objects.all()
    paginator = Paginator(ads_all, NUM_ADS_PER_PAGE)

    page = request.GET.get('page')
    try:
        ads_page = paginator.page(page)
    except PageNotAnInteger:
        ads_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    context = {
        'ads_list': ads_page
    }
    return render(request, 'textbook_app/ajax_ad_search.html', context)

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

@login_required
def ad_new(request):
    if request.method == 'POST':
        textbookForm = TextbookForm(request.POST)
        adForm = AdForm(request.POST)
        textbook_valid = textbookForm.is_valid()
        ad_valid = adForm.is_valid()
        if textbook_valid and ad_valid:
            textbook = textbookForm.save()
        # make sure the textbook form hasn't changed. If the user modified the data in the form,
        # then they are probably looking to add a new textbook,
        elif not textbookForm.has_changed() and 'existing-textbook' in request.POST and ad_valid:
            textbook = get_object_or_404(Textbook, pk=request.POST['existing-textbook'])
        else:
            # Return the form with any server side error messages (ex: ISBN already exists)
            return render(request, 'textbook_app/ad_new.html', {'textbookForm': textbookForm, 'adForm': adForm})
        ad = adForm.save(commit=False)
        ad.book = textbook
        ad.poster = request.user
        ad.save()
        return HttpResponseRedirect(reverse('textbook_app:ads'))
    else:
        textbookForm = TextbookForm()
        adForm = AdForm()
        return render(request, 'textbook_app/ad_new.html', {'textbookForm': textbookForm, 'adForm': adForm})

# TODO: Validate only the user that created the ad can edit, show error otherwise
# How do we handle non 2XX status codes? Redirect to error page?
@login_required
def ad_edit(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    textbook = get_object_or_404(Textbook, pk=ad.book.isbn)
    if request.method == 'POST':
        adForm = AdForm(request.POST, instance=ad)
        if adForm.is_valid():
            adForm.save()
            return HttpResponseRedirect(reverse('textbook_app:ads'))
    else:
        adForm = AdForm(instance=ad)
    return render(request, 'textbook_app/ad_edit.html', {'ad':ad, 'adForm': adForm, 'textbook':textbook})

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

def textbook_search(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''
    textbooks = Textbook.objects.filter(title__contains=search_text)
    return render_to_response('textbook_app/ajax_textbook_search.html', {'textbooks': textbooks})
