# Copyright Collab 2015-2019
# See LICENSE for details.

"""
URLConf for :py:mod:`require_i18n` tests.
"""

from django.contrib import admin

from django.conf.urls import include, url


admin.autodiscover()

urlpatterns = [
    url(r'^', include(admin.site.urls))
]
