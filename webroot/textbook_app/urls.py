from django.conf.urls import url

from . import views

app_name = 'textbook_app'

urlpatterns = [
    url(r'^ads_list/', views.ads_list, name='ads'),
    url(r'^ads/(?P<ad_id>[0-9]+)/edit', views.ad_edit, name='ad_edit'),
    url(r'^ads/(?P<ad_id>[0-9]+)', views.ad_detail, name='ad_detail'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^ad_new$', views.ad_new, name='ad_new'),
    url(r'^(?P<textbook_isbn>[0-9]+)/edit', views.textbook_edit, name='textbook_edit'),
    url(r'^textbook_search$', views.textbook_search, name='textbook_search'),
    url(r'^chat/(?P<receiver_user_id>[\w-]{,50})/$', views.chat, name='chat'),
    url(r'chat/send$', views.chat_send_message, name='chat_send_message')
]
