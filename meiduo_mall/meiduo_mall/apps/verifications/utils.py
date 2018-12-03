"""验证子应用工具

date: 18-12-3 下午8:16
"""
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """自定义jwt认证成功返回数据
    默认jwt认证成功只返回token, 添加返回用户ID和用户名

    :param token: 验证成功令牌
    :param user: 验证用户信息
    :param request: 请求报文
    """
    # 返回
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


class UsernameMobileAuthBackend(ModelBackend):
    """自定义扩展登陆接口, 支持手机登陆
    重写验证方法

    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """验证登录账号和密码是否正确 -- 重写验证方法

        :param request: 请求报文
        :param username: 登陆账号 ( 用户名/ 手机号码 )
        :param password: 密码
        """
        # 根据用户名或手机查询数据库
        query_set = User.objects.filter(Q(username=username) | Q(mobile=username))
        try:
            # 如果查询集存在
            if query_set.exists():
                # 获取数据 ( 取不到数据或存在多条数据都会报错 )
                user = query_set.get()
                # 如果验证密码正确
                if user.check_password(password):
                    # 返回用户信息
                    return user
        except Exception as e:
            print(e)
        return None
