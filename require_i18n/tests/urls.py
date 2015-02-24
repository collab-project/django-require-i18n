# Copyright Collab 2015

"""
URLConf for :py:mod:`require_i18n` tests.
"""

from django.contrib import admin
from django.conf.urls import patterns, include, url


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include(admin.site.urls)),
)
