#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls import url
from web.views import asset
from web.views import home


urlpatterns = [
    url(r'^cmdb.html$', home.CmdbView.as_view()),
    url(r'^asset.html$', asset.AssetListView.as_view()),
    url(r'^assets.html$', asset.AssetJsonView.as_view()),
]