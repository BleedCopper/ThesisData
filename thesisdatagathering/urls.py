from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='thesis.html'), name='thesis'),
    url(r'^thesis/$', TemplateView.as_view(template_name='thesis.html'), name='thesis'),
    url(r'^data-requirements/$', TemplateView.as_view(template_name='data-requirements.html'), name='datarequirements'),
    url(r'^thesis/data-requirements/$', TemplateView.as_view(template_name='data-requirements.html'), name='datarequirements'),
    url(r'^data-collection/$', TemplateView.as_view(template_name='data-collection.html'), name='datacollection'),
    url(r'^data-requirements/data-collection/$', TemplateView.as_view(template_name='data-collection.html'), name='datacollection'),
    url(r'^auth/?$', views.auth, name='oauth_auth'),
    url(r'^thanks/?$', views.thanks, name="twitter_callback"),
    url(r'^facebookhandler/?$', views.facebookhandler, name="facebookhandler"),
]
