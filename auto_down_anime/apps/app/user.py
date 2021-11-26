# -*- coding:utf-8 -*-
import requests
import turbo.log
from .base import BaseHandler

logger = turbo.log.getLogger(__file__)


class LoginHandler(BaseHandler):

    def GET(self, type):
        self.route(type)

    def POST(self, type):
        self.route(type)

    def do_tel(self):
        tel = int(self.get_argument('tel', '0'))
        code = self.get_argument('code', '')
        device_id = self.get_argument('device_id', '')
        package_name = self.get_argument('package_name', '')
        self._data = user.login_telcode(tel, code, device_id, package_name)


    def do_other(self):
        open_id = self.get_argument('open_id', '')
        device_id = self.get_argument('device_id', '')
        avatar = self.get_argument('avatar', '')
        package_name = self.get_argument('package_name', '')
        self._data = user.login_other(open_id, avatar, device_id, package_name)


    def do_send_code(self):
        tel = int(self.get_argument('tel', '0'))
        self._data = user.send_telcode(tel)


    def do_info(self):
        token = self.get_argument('token', '')
        self._data = user.get_user_info(token)


class InfoHandler(BaseHandler):

    def GET(self):
        token = self.get_argument('token', '')
        self._data = user.get_user_info(token)


class TaskHandler(BaseHandler):

    def GET(self, type):
        self.route(type)

    def POST(self, type):
        self.GET(type)

    def do_list(self):
        token = self.get_argument('token', '')
        os = self.get_argument('os', '')
        package_name = self.get_argument('package_name', '')
        self._data = user_task.list(token, os, package_name)

    def do_report(self):
        token = self.get_argument('token', '')
        type = self.get_argument('type', '')
        task_id = self.get_argument('task_id', '')
        data = self.get_argument('data', '')
        number = self.get_argument('number', '1')
        self._data = user_task.report(token, type, task_id, data, number)


class CouponHandler(BaseHandler):

    def GET(self, type):
        self.route(type)

    def POST(self, type):
        self.GET(type)

    def do_list(self):
        token = self.get_argument('token', '')
        os = self.get_argument('os', '')
        package_name = self.get_argument('package_name', '')
        self._data = user_coupon.list(token, os, package_name)


class VipHandler(BaseHandler):

    def GET(self, type):
        self.route(type)

    def POST(self, type):
        self.GET(type)

    def do_list(self):
        os = self.get_argument('os', '')
        package_name = self.get_argument('package_name', '')
        self._data = buy_vip.get_vip_list(os, package_name)
        pass

    def do_get_price(self):
        token = self.get_argument('token', '')
        os = self.get_argument('os', '')
        package_name = self.get_argument('package_name', '')
        coupons = self.get_argument('coupons', 'all')
        self._data = buy_vip.get_all_price(token, os, package_name, coupons)


class BuyHandler(BaseHandler):

    def GET(self, platform, type):
        self.route('%s_%s' % (platform, type))

    def POST(self, platform, type):
        self.GET(platform, type)

    def do_alipay_sign(self):
        token = self.get_argument('token', '')
        os = self.get_argument('os', '')
        vip_id = self.get_argument('vip_id', '')
        package_name = self.get_argument('package_name', '')
        coupons = self.get_argument('coupons', 'all')
        self._data = buy_vip.Alipay.create(token, os, package_name, vip_id, self.request.remote_ip, coupons)

    def do_alipay_notify(self):
        pass

    def do_wechat_sign(self):
        token = self.get_argument('token', '')
        os = self.get_argument('os', '')
        vip_id = self.get_argument('vip_id', '')
        package_name = self.get_argument('package_name', '')
        coupons = self.get_argument('coupons', 'all')
        params, out_trade_no = buy_vip.Wechat.create(token, os, package_name, vip_id, self.request.remote_ip, coupons)
        self._data = {
            'params': params,
            'oid': out_trade_no,
        }

    def do_wechat_notify(self):
        pass
