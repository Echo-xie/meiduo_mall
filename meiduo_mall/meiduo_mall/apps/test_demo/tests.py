"""子应用开发测试用例, 单元测试

"""
from django.test import TestCase


class ModeTest(TestCase):

    def setUp(self):
        """每个test函数调用前调用
        :return:
        """
        super(ModeTest, self).setUp()
        print("测试函数调用前")

    def tearDown(self):
        """每个test函数调用后调用
        :return:
        """
        super(ModeTest, self).tearDown()
        print("测试函数调用后")

    def test_xxx(self):
        """单元测试, 测试一个功能
        :return:
        """
        print("test...test...1111111111")

    def test_two(self):
        """单元测试, 测试一个功能
        :return:
        """
        print("test...test...2222222222")

    def test_add(self):
        """添加数据

        :return:
        """
        print("???????????????")

    def runTest(self):
        """运行具体测试, 自定义测试调用
        :return:
        """
        # self.test_one()
        # self.test_two()


if __name__ == '__main__':
    # 运行测试类的具体测试
    # ModeTest().runTest()
    pass
