from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='thesis.html'), name='thesis'),
    url(r'^auth/?$', views.auth, name='oauth_auth'),
    url(r'^thanks/?$', views.thanks, name="twitter_callback"),
    url(r'^facebookhandler/?$', views.facebookhandler, name="facebookhandler"),
]
