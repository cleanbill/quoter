from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('core.views',
    (r'quote/(?P<quote_token>.+)$','quote'),
    (r'toggle/(?P<quote_token>.+)$','toggle'),
    (r'/404','nowhere'),
    (r'$','jumpin'),
    (r'print/(?P<quote_token>.+)$','printQuote')
)
                   
handler404 = 'core.views.404'
