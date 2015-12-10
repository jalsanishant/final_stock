from django.conf.urls import patterns,include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Examples:
    url(r'^$', 'market2.views.index'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/','market2.views.index',name='index'),
    url(r'^registerPage/$','market2.views.registerPage',name='registerPage'),
    url(r'^loginPage/$','market2.views.loginPage',name='loginPage'),
    url(r'^register/$','market2.views.register',name='register'),
    url(r'^login/$','market2.views.login',name='login'),
    url(r'^logout/$','market2.views.logout',name='logout'),
    url(r'^help/$','market2.views.help',name='help'),
    url(r'^search/$','market2.views.search',{'query': None}),
    url(r'^profile/$','market2.views.portagraph'),
    
    url(r'^search/(?P<query>.*)/$', 'market2.views.search'),
    url(r'^stock/(?P<symbol>\w+)/$', 'market2.views.show_stock'),

    url(r'^buy/$', 'market2.views.handle_buy'),
    url(r'^sell/$', 'market2.views.handle_sell'),

    #url(r'^leaders/$', 'market2.views.show_leaders'),
    url(r'^leaders/$', 'market2.views.fn'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)