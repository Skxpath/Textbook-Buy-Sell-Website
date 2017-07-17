from django.conf.urls import url

from .views import signup
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', auth_views.login, name='login'),
    # When the user logs out, go back to the login page
    url(r'^logout/$', auth_views.logout,  {'next_page': 'accounts:login'}, name='logout'),
]
