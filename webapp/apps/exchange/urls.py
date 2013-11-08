from django.conf.urls import patterns, url

urlpatterns = patterns('webapp.apps.exchange.views',
    url(r'^$', 'list', name='exchange-list'),
    url(r'^create/$', 'create', name='exchange-create'),
    url(r'^(?P<exchange_id>\d+)/edit/$', 'edit', name='exchange-edit'),
    url(r'^(?P<exchange_id>\d+)/delete/$', 'delete', name='exchange-delete'),
)
