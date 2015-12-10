from django.conf.urls.defaults import *

urlpatterns = patterns('stocksite.market.views',
    (r'^$', 'index'),
    
    (r'^register/$', 'register'),
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),

    (r'^help/$', 'help'),

    (r'^search/$', 'search', {'query': None}),
    (r'^search/(?P<query>.*)/$', 'search'),
    (r'^stock/(?P<symbol>\w+)/$', 'show_stock'),

    (r'^buy/$', 'handle_buy'),
    (r'^sell/$', 'handle_sell'),

    (r'^leaders/$', 'show_leaders'),
)
