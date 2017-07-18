from django.conf.urls import url

from . import views

app_name = 'textbook_app'

urlpatterns = [
    url(r'^ads_list/', views.ads_list, name='ads'),
    url(r'^ads/(?P<ad_id>[0-9]+)/edit', views.ad_edit, name='ad_edit'),
    url(r'^ads/(?P<ad_id>[0-9]+)', views.ad_detail, name='ad_detail'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^ads_new$', views.ads_new, name='ads_new'),
    url(r'^(?P<textbook_isbn>[0-9]+)/edit', views.textbook_edit, name='textbook_edit'),
    url(r'^ads_new$', views.ads_new, name='ads_new'),
    url(r'^textbook_search$', views.textbook_search, name='textbook_search')
]
