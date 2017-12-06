#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from repository import models
from web import forms
from web.service import user
from .home import auth


@method_decorator(auth, name='dispatch')
class UserListView(View):
    def get(self, request, *args, **kwargs):
        username = request.session.get('username')
        return render(request, 'user_list.html', locals())


class UserJsonView(View):
    def get(self, request):
        obj = user.UserProfile()
        response = obj.fetch_users(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = user.UserProfile.delete_users(request)
        return JsonResponse(response.__dict__)

    @method_decorator(csrf_exempt)
    def put(self, request):
        response = user.UserProfile.put_users(request)
        return JsonResponse(response.__dict__)


class EditUserView(View):
    def get(self, request, status, user_nid):
        condition = {"status": status, "id": user_nid}
        user = models.UserProfile.objects.filter(**condition).first()
        obj_form = forms.UserModelForm(instance=user)
        return render(request, "user_change.html", locals())

    def post(self, request, status, user_nid):
        condition = {"status": status, "id": user_nid}
        user = models.UserProfile.objects.filter(**condition).first()
        obj_form = forms.UserModelForm(request.POST, instance=user)
        if obj_form.is_valid():
            obj_form.save()
            print(obj_form.errors.as_json())
        return render(request, "user_change.html", locals())


class AddUserView(View):
    def get(self, request):
        obj_form = forms.UserModelForm()
        return render(request, "user_add.html", locals())

    def post(self, request):
        obj_form = forms.UserModelForm(request.POST)
        if obj_form.is_valid():
            obj_form.save()
        return render(request, "user_add.html", locals())
