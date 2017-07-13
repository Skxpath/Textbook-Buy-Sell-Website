from django.conf.urls import url

from . import views

app_name = 'textbook_app'

urlpatterns = [
    # Pages
    url(r'^ads_list/$', views.ads_list, name='ads'),
    # url(r'^contact_info/(?P<contact_id>[0-9]+)$', views.contactinfo, name='contact_info'),
]
