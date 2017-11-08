#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views import View
from django.shortcuts import render
from django.http import JsonResponse


class CmdbView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'layout/_layout.html')