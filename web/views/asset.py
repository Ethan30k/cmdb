#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from repository import models
from web import forms

from web.service import asset


class AssetListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'asset_list.html')


class AssetJsonView(View):
    def get(self, request):
        obj = asset.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = asset.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    @method_decorator(csrf_exempt)
    def put(self, request):
        response = asset.Asset.put_assets(request)
        return JsonResponse(response.__dict__)


class AssetDetailView(View):
    def get(self, request, device_type_id, asset_nid):
        response = asset.Asset.assets_detail(device_type_id, asset_nid)
        return render(request, 'asset_detail.html', {'response': response, 'device_type_id': device_type_id})


class EditAssetView(View):
    def get(self, request, device_type_id, asset_nid):
        condition = {"device_type_id": device_type_id, "id": asset_nid}
        asset = models.Asset.objects.filter(**condition)

        model_form = forms.CreateModelForm(request, obj=models.Asset)
        if request.method == "GET":
            obj_form = model_form(instance=asset)
        elif request.method == "POST":
            obj_form = model_form(instance=asset, data=request.POST)
            if obj_form.is_valid():
                obj_form.save()
            # print(obj_form)
        return render(request, "asset_change.html", locals())


class AddAssetView(View):
    def get(self, request, device_type_id, asset_nid):

        model_form = forms.CreateModelForm(request, obj=models.Asset)
        if request.method == "GET":
            obj_form = model_form(instance=asset)
        elif request.method == "POST":
            obj_form = model_form(instance=asset, data=request.POST)
            if obj_form.is_valid():
                obj_form.save()
            # print(obj_form)
        return render(request, "asset_change.html", locals())