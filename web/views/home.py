#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views import View
from django.shortcuts import render
from django.http import JsonResponse


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class CmdbView(View):
    def get(self, request, *args, **kwargs):
        # return render(request, 'layout/_layout.html')
        return render(request, 'asset_list.html')