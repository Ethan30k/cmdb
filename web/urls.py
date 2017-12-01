#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls import url
from web.views import asset
from web.views import home
from web.views import user


urlpatterns = [
    url(r'^index.html$', home.IndexView.as_view()),
    url(r'^cmdb.html$', home.CmdbView.as_view()),
    url(r'^asset.html$', asset.AssetListView.as_view()),
    url(r'^assets.html$', asset.AssetJsonView.as_view()),
    url(r'^asset-(?P<device_type_id>\d+)-(?P<asset_nid>\d+).html$', asset.AssetDetailView.as_view()),
    url(r'^add-asset.html$', asset.AddAssetView.as_view()),
    url(r'^edit-asset-(?P<device_type_id>\d+)-(?P<asset_nid>\d+).html$', asset.EditAssetView.as_view()),
    url(r'^login.html$', home.Login.as_view()),
    url(r'^logout.html$', home.Logout.as_view()),
    url(r'^user.html$', user.UserListView.as_view()),
    url(r'^users.html$', user.UserJsonView.as_view()),
    url(r'^add-user.html$', user.AddUserView.as_view()),
    url(r'^edit-user-(?P<status>\d+)-(?P<user_nid>\d+).html$', user.EditUserView.as_view()),
]