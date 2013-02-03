# !/usr/bin/env python
# ===============================================================================
# This file is part of PyPWSafe.
# 
#    PyPWSafe is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
# 
#    PyPWSafe is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
# 
#    You should have received a copy of the GNU General Public License
#    along with PyPWSafe.  If not, see http://www.gnu.org/licenses/old-licenses/gpl-2.0.html 
# ===============================================================================
from django.conf.urls.defaults import patterns, include, url  # @UnresolvedImport

# Uncomment the next two lines to enable the admin:
from django.contrib import admin  # @UnresolvedImport
admin.autodiscover()
from dajaxice.core import dajaxice_autodiscover  # @UnresolvedImport
dajaxice_autodiscover()
from django.conf import settings

urlpatterns = patterns('',
    # XML-RPC and JSON RPC Access
    (r'^RPC2$', 'rpc4django.views.serve_rpc_request'),
    # Dajax
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),

    # Psafe site
    (r'^pws(?:/)?', include('psafefe.psafe.urls')),
    # Psafe site
    (r'^psafe(?:/)?', include('psafefe.psafe.urls')),
    
    # Admin site
    (r'^admin/', include(admin.site.urls)),
    
    # Misc static pages
    (r'^(?:/)?$', 'psafefe.psafe.views.static.rootIndex'),
    (r'^robots\.txt(?:/)?$', 'psafefe.psafe.views.static.robots'),
    (r'^crossdomain\.xml(?:/)?$', 'psafefe.psafe.views.static.crossdomain'),

    # Account junk
    (r'^accounts/login(?:/)?$', 'django.contrib.auth.views.login', dict(redirect_field_name = '/index.html')),
    (r'^accounts/logout(?:/)?$', 'django.contrib.auth.views.logout_then_login'),
    # Let users edit their profile
    # (r'^accounts/profile(?:/)?$', 'psafefe.psafe.views.profile.edit'),
    # Let users change their password
    (r'^accounts/changepassword(?:/)?$', 'django.contrib.auth.views.password_change'),
    (r'^accounts/password/done(?:/)?$', 'django.contrib.auth.views.password_change_done'),
    # Password reset
    (r'^password_reset(?:/)?$', 'django.contrib.auth.views.password_reset'),
    (r'^password_reset/done(?:/)?$', 'django.contrib.auth.views.password_reset_done'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)(?:/)?$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done(?:/)?$', 'django.contrib.auth.views.password_reset_complete'),
    # User registration
#    (r'^accounts/register(?:/)?$', 'psafefe.psafe.views.profile.register'),
#    (r'^accounts/confirm/([a-zA-Z0-9]+)(?:/)?$', 'psafefe.psafe.views.profile.confirm'),
)
