#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator


def auth(func):
    def inner(request, *args, **kwargs):
        if not request.session.get('is_login', None):
            return redirect('/login.html')
        return func(request, *args, **kwargs)
    return inner


@method_decorator(auth, name='dispatch')
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


@method_decorator(auth, name='dispatch')
class CmdbView(View):
    def get(self, request, *args, **kwargs):
        username = request.session.get('username')
        return render(request, 'asset_list.html', locals())


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        if user == 'chengyiqiang' and pwd == '123':
            request.session['username'] = user
            request.session['is_login'] = True
            print(request.POST.get('rmb'))
            if request.POST.get('rmb') == '1':
                request.session.set_expiry(10)
            return redirect('/cmdb.html')
        else:
            return redirect('/login.html')


class Logout(View):
    def get(self, request):
        request.session.clear()
        return redirect('/login.html')