# Copyright Collab 2015-2016
# See LICENSE for details.

"""
URLConf for :py:mod:`require_i18n` tests.
"""

from django.contrib import admin
from django.conf.urls import patterns, include, url


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include(admin.site.urls)),
)
