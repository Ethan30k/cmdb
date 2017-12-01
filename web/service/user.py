#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from .base import BaseServiceList
from django.http.request import QueryDict


class UserProfile(BaseServiceList):
    def __init__(self):
        condition_config = [
            {'name': 'name', 'text': '姓名', 'condition_type': 'input'},
            {'name': 'email', 'text': '邮箱', 'condition_type': 'input'},
            {'name': 'role_id', 'text': '角色名', 'condition_type': 'select', 'global_name': 'role_list'},
            {'name': 'status', 'text': '状态', 'condition_type': 'select', 'global_name': 'user_status_list'}
        ]

        table_config = [
            {
                'q': 'id',  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
                'title': "ID",  # 前段表格中显示的标题
                'display': 1,  # 是否在前段显示，0表示在前端不显示, 1表示在前端隐藏, 2表示在前段显示
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},
                'attr': {}  # 自定义属性
            },
            {
                'q': 'name',
                'title': '姓名',
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@name'}},
                'attr': {}
            },
            {
                'q': 'email',
                'title': '电子邮件',
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@email'}},
                'attr': {}
            },
            {
                'q': 'phone',
                'title': '手机',
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@phone'}},
                'attr': {}
            },
            {
                'q': 'role',
                'title': '角色名',
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@@role_list'}},
                'attr': {'name': 'role', 'id': '@role', 'original': '@role', 'edit-enable': 'true',
                         'global-name': 'role_list',
                         'edit-type': 'select'}
            },
            {
                'q': 'status',
                'title': '状态',
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@@user_status_list'}},
                'attr': {'name': 'status', 'id': '@status', 'original': '@status', 'edit-enable': 'true',
                         'global-name': 'user_status_list',
                         'edit-type': 'select'}
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': "<a href='/edit-user-{status}-{nid}.html'>编辑</a>",
                    'kwargs': {'status': '@status', 'nid': '@id'}},
                'attr': {}
            },
        ]

        extra_select = {

        }
        super(UserProfile, self).__init__(condition_config, table_config, extra_select)

    @property
    def role_list(self):
        values = models.Role.objects.only('id', 'name')
        result = map(lambda x: {'id': x.id, 'name': "%s" % x.name}, values)
        return list(result)

    @property
    def user_status_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.UserProfile.status_choice)
        return list(result)

    @staticmethod
    def users_condition(request):
        con_str = request.GET.get('condition', None)
        if not con_str:
            con_dict = {}
        else:
            con_dict = json.loads(con_str)

        con_q = Q()
        for k, v in con_dict.items():
            temp = Q()
            temp.connector = 'OR'
            for item in v:
                temp.children.append((k, item))
            con_q.add(temp, 'AND')
        return con_q

    def fetch_users(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.users_condition(request)
            users_count = models.UserProfile.objects.filter(conditions).count()
            peritems = int(request.GET.get('peritems', None))
            page_info = PageInfo(request.GET.get('pager', None), users_count, peritems)
            users_list = models.UserProfile.objects.filter(conditions).extra(select=self.extra_select).values(
                *self.values_list)[page_info.start:page_info.end]

            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['data_list'] = list(users_list)
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            ret['global_dict'] = {
                'role_list': self.role_list,
                'user_status_list': self.user_status_list,
            }
            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        print(response)
        return response

    @staticmethod
    def delete_users(request):
        response = BaseResponse()
        try:
            print(request.body)
            delete_dict = QueryDict(request.body, encoding='utf-8')
            id_list = delete_dict.getlist('id_list')
            models.UserProfile.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def put_users(request):
        response = BaseResponse()
        try:
            response.error = []
            put_dict = QueryDict(request.body, encoding='utf-8')
            update_list = json.loads(put_dict.get('update_list'))
            error_count = 0
            for row_dict in update_list:
                nid = row_dict.pop('nid')
                num = row_dict.pop('num')
                try:
                    models.UserProfile.objects.filter(id=nid).update(**row_dict)
                except Exception as e:
                    response.error.append({'num': num, 'message': str(e)})
                    response.status = False
                    error_count += 1
            if error_count:
                response.message = '共%s条,失败%s条' % (len(update_list), error_count,)
            else:
                response.message = '更新成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response
