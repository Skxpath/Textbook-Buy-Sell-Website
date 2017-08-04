from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from .models import Ad, Textbook, AdForm, TextbookForm, TextbookFormNoIsbn, Chat, Message
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone

# TODO: Let users set this value from a form field
NUM_ADS_PER_PAGE = 5

def ads_list(request):
    if (request.GET.__contains__('ad-search-text')):
        search_text = request.GET.get('ad-search-text')
    else:
        search_text = ''
    ads_all = Ad.objects.filter(book__title__contains=search_text)
    paginator = Paginator(ads_all, NUM_ADS_PER_PAGE)

    page = request.GET.get('page')
    search = request.GET.get('ad-search-text')
    print(search)
    try:
        ads_page = paginator.page(page)
    except PageNotAnInteger:
        ads_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        ads_page = paginator.page(paginator.num_pages)
    context = {
        # Note: the user may not be present here since login isn't required for this page
        'user': request.user,
        'ads_list': ads_page,
        'previous_search_text': search_text
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

def ad_delete(request, ad_id):
    ad_tobe_deleted = get_object_or_404(Ad, pk=ad_id)
    ad_tobe_deleted.delete()
    return HttpResponseRedirect(reverse('textbook_app:profile'))


# This function is horrendously complex... sorry!
# TODO: make this less complex
def ad_new_or_edit(request, isEditAd, ad_id):
    if isEditAd:
        ad = get_object_or_404(Ad, pk=ad_id)
    if request.method == 'POST':
        textbookForm = TextbookForm(request.POST)
        if isEditAd:
            adForm = AdForm(request.POST, instance=ad)
        else:
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
            if isEditAd:
                context = {'ad': ad, 'textbookForm': textbookForm, 'adForm': adForm}
            else:
                context = {'textbookForm': textbookForm, 'adForm': adForm}
            # Return the form with any server side error messages (ex: ISBN already exists)
            return render(request, 'textbook_app/ad_new_or_edit.html', context)
        ad = adForm.save(commit=False)
        ad.book = textbook
        ad.poster = request.user
        ad.save()
        if isEditAd:
            return HttpResponseRedirect(reverse('textbook_app:profile'))
        else:
            return HttpResponseRedirect(reverse('textbook_app:ads'))
    else:
        textbookForm = TextbookForm()
        if isEditAd:
            adForm = AdForm(instance=ad)
            context = {'ad': ad, 'textbookForm': textbookForm, 'adForm': adForm}
        else:
            adForm = AdForm()
            context = {'textbookForm': textbookForm, 'adForm': adForm}
        return render(request, 'textbook_app/ad_new_or_edit.html', context)

@login_required
def ad_new(request):
    return ad_new_or_edit(request, False, 1)

# TODO: Validate only the user that created the ad can edit, show error otherwise
# How do we handle non 2XX status codes? Redirect to error page?
@login_required
def ad_edit(request, ad_id):
    return ad_new_or_edit(request, True, ad_id)

@login_required
def textbook_edit(request, textbook_isbn):
    textbook = get_object_or_404(Textbook, pk=textbook_isbn)
    if request.method == "POST":
        textbookForm = TextbookFormNoIsbn(request.POST, instance=textbook)
        if textbookForm.is_valid():
            textbookForm.save()
            return HttpResponseRedirect(reverse('textbook_app:ads'))
        else:
            return render(request, "textbook_app/textbook_edit.html", {'textbook': textbook, 'textbookForm': textbookForm})
    else:
        textbookForm = TextbookFormNoIsbn(instance=textbook)
        return render(request, "textbook_app/textbook_edit.html", {'textbook': textbook, 'textbookForm': textbookForm})

def textbook_search(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''
    textbooks = Textbook.objects.filter(title__contains=search_text)
    return render_to_response('textbook_app/ajax_textbook_search.html', {'textbooks': textbooks})

@login_required
def chat(request, receiver_user_id):
    receiver_user = get_object_or_404(get_user_model(), pk=receiver_user_id)
    chats = Chat.objects.filter(users=request.user).filter(users=receiver_user)
    # If a chat doesn't exist, display an empty messages page
    if chats.count() < 1:
        context = {
            'sender': request.user,
            'receiver': receiver_user,
        }
    else:
        # If a chat exists, get the first match (there should only be one chat between two users)
        chat = chats[0]
        # We want to show the last 50 messages, ordered most-recent-last
        numMessagesToDisplay = 50
        messages = chat.messages.order_by('-timestamp')[:numMessagesToDisplay].reverse()
        context = {
            'sender': request.user,
            'receiver': receiver_user,
            'messages': messages,
        }
    return render(request, "textbook_app/chat_messages.html", context)

@login_required
def chat_send_message(request):
    if request.method == 'POST':
        receiver_user_id = request.POST['receiver_user_id']
        receiver = get_object_or_404(get_user_model(), pk=receiver_user_id)
        chats = Chat.objects.filter(users=request.user).filter(users=receiver)
        # Create a new chat upon sending of first message if a chat doesn't exist
        # TODO: fix race condition that could occur if two people tried to make a chat with one another at the same time
        # probably using database transactions or something
        if (chats.count() < 1):
            chat = Chat()
            chat.save()
            chat.users.add(request.user, receiver)
            chat.save()
        else:
            chat = chats[0]

        message = Message(chat=chat, user=request.user, message=request.POST['message'], timestamp=timezone.now())
        message.save()
        return HttpResponseRedirect(reverse('textbook_app:chat', kwargs={'receiver_user_id': receiver.id}))
    else:
        return Http404("This url only accepts POST requests")

@login_required
def chat_list(request):
    user_chats = Chat.objects.filter(users=request.user)
    recipient_users_list = []
    for chat in user_chats:
        for user in chat.users.all():
            if user != request.user:
                recipient_users_list.append(user)
    return render(request, "textbook_app/chat_list.html", {'chat_recipient_list': recipient_users_list})
