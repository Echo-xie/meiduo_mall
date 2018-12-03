from django.test import TestCase, Client

from meiduo_mall.utils.common import get_sms_code_by_mobile
from verifications import views


# Create your tests here.

class VmTestCase(TestCase):

    def test_send_sms_code(self):
        """发送手机短信验证码"""
        #
        print("test---------------发送手机短信验证码")
        # 测试浏览器
        test_client = Client()
        # 请求路径
        path = "/vm/mobile/13000000000/count/"
        # 请求体
        data = {}
        # 浏览器get请求, 获取响应
        resp = test_client.get(path)
        #
        print(resp.data)
        # 断言结果
        self.assertTrue(resp.status_code == 200)

    def test_username_repeat(self):
        """用户名重复"""
        #
        print("test---------------用户名重复")
        # 测试浏览器
        test_client = Client()
        # 请求路径
        path = "/vm/username/admin/count/"
        # 请求体
        data = {}
        # 浏览器get请求, 获取响应
        resp = test_client.get(path)
        #
        print(resp.data)
        # 断言结果
        self.assertTrue(resp.status_code == 200)

    def test_user_mobile_repeat(self):
        """用户手机重复"""
        #
        print("test---------------用户手机重复")
        # 测试浏览器
        test_client = Client()
        # 请求路径
        path = "/vm/mobile/13000000000/count/"
        # 请求体
        data = {}
        # 浏览器get请求, 获取响应
        resp = test_client.get(path)
        #
        print(resp.data)
        # 断言结果
        self.assertTrue(resp.status_code == 200)

    def test_user_register(self):
        """用户注册"""
        #
        print("test---------------用户注册")
        # 测试浏览器
        test_client = Client()
        # 请求路径 -- 用户注册
        register_path = "/vm/user_register/"
        # 手机号码
        mobile = 13300000001
        # 获取手机短信验证码
        sms_code_path = "/vm/sms_code/" + str(mobile) + "/"
        # 获取手机短信验证码
        sms_code_resp = test_client.get(sms_code_path)
        # 判断手机验证码是否获取成功
        self.assertTrue((sms_code_resp.status_code == 200) or (sms_code_resp.status_code == 400))
        # 通过通用工具获取手机验证码
        sms_code = get_sms_code_by_mobile(mobile=mobile)
        # 请求体
        data = {
            "username": "test_1",
            "password": "123123123",
            "password2": "123123123",
            "mobile": 13300000001,
            "sms_code": sms_code,
            "allow": True,
        }
        # 浏览器post请求用户注册, 获取响应
        resp = test_client.post(path=register_path, data=data)
        #
        print(resp.data)
        # 断言结果
        self.assertTrue(resp.status_code == 201)
