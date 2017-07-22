from django.conf.urls import url

from . import views

app_name = 'textbook_app'

urlpatterns = [
    url(r'^ads_list/', views.ads_list, name='ads'),
    url(r'^ads/(?P<ad_id>[0-9]+)/edit', views.ad_edit, name='ad_edit'),
    url(r'^ads/(?P<ad_id>[0-9]+)', views.ad_detail, name='ad_detail'),
    url(r'^profile/$', views.profile, name='profile'),
    # TODO: see if it's possible to have the same urls but different views for GET and POST requests
    url(r'^ads_new$', views.ads_new, name='ads_new'),
    url(r'^(?P<textbook_isbn>[0-9]+)/edit', views.textbook_edit, name='textbook_edit'),
    # example of url parameter capturing for reference
    # url(r'^contact_info/(?P<contact_id>[0-9]+)$', views.contactinfo, name='contact_info'),
]
