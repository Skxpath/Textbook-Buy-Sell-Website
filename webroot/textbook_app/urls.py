from django.conf.urls import url

from . import views

app_name = 'textbook_app'

urlpatterns = [
    url(r'^ads_list/$', views.ads_list, name='ads'),
    url(r'^profile/$', views.profile, name='profile'),
    # TODO: see if it's possible to have the same urls but different views for GET and POST requests
    url(r'^ads_new_page$', views.ads_new_page, name='ads_new_page'),
    url(r'^ads_new_request', views.ads_new_request, name='ads_new_request'),
    # example of url parameter capturing for reference
    # url(r'^contact_info/(?P<contact_id>[0-9]+)$', views.contactinfo, name='contact_info'),
]
