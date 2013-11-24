from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView, TemplateView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^$', RedirectView.as_view(url='/exchange/'), name='home'),
    url(r'^login/$', TemplateView.as_view(template_name='accounts/login.html'), name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^exchange/', include('webapp.apps.exchange.urls')),
)
