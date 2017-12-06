#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import forms
from django.forms import widgets
from repository import models


class AssetModelForm(forms.ModelForm):
    class Meta:
        model = models.Asset
        exclude = ['latest_date', 'create_date']

        # widgets = {
        #         'device_type_id': widgets.Textarea(attrs={'class': 'form-control', 'id': 'demo-is-inputnormal',
        #         'placeholder': ''})
        #     }


class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        exclude = ['password']
