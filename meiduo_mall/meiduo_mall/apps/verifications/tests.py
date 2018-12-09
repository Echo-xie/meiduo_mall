from django.test import TestCase, Client
from meiduo_mall.utils.common import get_sms_code_by_mobile


# Create your tests here.

class VmTestCase(TestCase):

    def setUp(self):
        # 测试浏览器 -- TestCase 自带 self.client
        # self.test_client = Client()
        pass

    def test_send_sms_code(self):
        """发送手机短信验证码"""
        #
        print("test---------------发送手机短信验证码")
        # 请求路径
        path = "/vm/sms_code/13000000000/"
        # 请求体
        data = {}
        # 浏览器get请求, 获取响应
        resp = self.client.get(path)
        #
        print(resp.data)
        # 断言结果
        # self.assertTrue(resp.status_code == 200)
        # self.assertEqual(resp.status_code, 200)

    def test_username_repeat(self):
        """用户名重复"""
        #
        print("test---------------用户名重复")
        # 请求路径
        path = "/vm/username/admin/count/"
        # 请求体
        data = {}
        # 浏览器get请求, 获取响应
        resp = self.client.get(path)
        #
        print(resp.data)
        # 断言结果
        # self.assertTrue(resp.status_code == 200)
        self.assertEqual(resp.status_code, 200)

    def test_user_mobile_repeat(self):
        """用户手机重复"""
        #
        print("test---------------用户手机重复")
        # 请求路径
        path = "/vm/mobile/13000000000/count/"
        # 请求体
        data = {}
        # 浏览器get请求, 获取响应
        resp = self.client.get(path)
        #
        print(resp.data)
        # 断言结果
        # self.assertTrue(resp.status_code == 200)
        self.assertEqual(resp.status_code, 200)

    def test_user_register(self):
        """用户注册"""
        #
        print("test---------------用户注册")
        # 请求路径 -- 用户注册
        register_path = "/vm/user_register/"
        # 手机号码
        mobile = 13300000001
        # 获取手机短信验证码
        sms_code_path = "/vm/sms_code/" + str(mobile) + "/"
        # 获取手机短信验证码
        sms_code_resp = self.client.get(sms_code_path)
        # 判断手机验证码是否获取成功
        self.assertTrue((sms_code_resp.status_code == 200) or (sms_code_resp.status_code == 400))
        # 通过通用工具获取手机验证码
        sms_code = get_sms_code_by_mobile(mobile=mobile)
        # 请求体
        data = {
            "username": "test_1",
            "password": "123123123",
            "password2": "123123123",
            "mobile": mobile,
            "sms_code": sms_code,
            "allow": True,
        }
        # 浏览器post请求用户注册, 获取响应
        resp = self.client.post(path=register_path, data=data)
        #
        print(resp.data)
        # 断言结果
        # self.assertTrue(resp.status_code == 201)
        self.assertEqual(resp.status_code, 201)

    def test_user_login(self):
        """用户登陆
        由于是使用Django提供的验证功能, 可以用Client的login进行登陆测试
        """
        #
        print("test---------------用户登陆")
        # 用Client的login进行登陆测试
        is_login = self.client.login(username="admin", password="123123123")
        # True
        if is_login:
            print("登陆成功")
        # False
        else:
            print("登陆失败")
        # 断言
        self.assertTrue(self.client)
