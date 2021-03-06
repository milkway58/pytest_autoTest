#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Meng xiangguo <mxgnene01@gmail.com>
#
#              _____               ______
#     ____====  ]OO|_n_n__][.      |    |]
#    [________]_|__|________)<     |MENG|
#     oo    oo  'oo OOOO-| oo\_   ~o~~~o~'
# +--+--+--+--+--+--+--+--+--+--+--+--+--+
#                        2019-09-18  09:53

import json
import allure
import pytest
import requests
from conf.sysconfig import UC_HOST
from dutil.res_diff import res_diff
from dutil.find_case import findCase
from dutil.make_ddt import MakeDdt

casepath = findCase(__file__, 'uc_inner_invite.yml', n=2)
test_cases = MakeDdt(casepath).makeData_V2()


class TestUcenterInnerInvite():
    '''
    基于 yaml 文件数据的自动化case
    '''
    @allure.title("{name}")
    @pytest.mark.parametrize("method, url, params, data, headers, cookies, proxies, status_code, expectData, name",
                             test_cases)
    def test_success(self, method, url, params, data, headers, cookies, proxies, status_code, expectData, name):
        '''/inner/invite'''
        allure.attach('{0}'.format(url), name='请求url', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(headers)), name='请求headers', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(params)), name='请求param', attachment_type=allure.attachment_type.TEXT)
        allure.attach('{0}'.format(json.dumps(data)), name='请求data', attachment_type=allure.attachment_type.TEXT)

        res = requests.request(method, url, params=params, data=data, headers=headers, cookies=cookies, proxies=proxies)
        allure.attach('{0}'.format(json.dumps(res.json())), name='响应结果', attachment_type=allure.attachment_type.TEXT)

        assert status_code == res.status_code
        assert {} == res_diff(expectData, res.json())


    @allure.title("查询最大 invite ID")
    def test_invite_queryMaxId(self, uc_db):
        '''/xc_uc/inner/invite/queryMaxId.do'''
        url = UC_HOST + "/xc_uc/inner/invite/queryMaxId.do"
        res = requests.get(url)

        db_res = uc_db.query("select max(id) as id from t_user_free_invite_record")
        assert 200 == res.status_code
        assert db_res.one().id == res.json()['data']