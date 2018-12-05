"""

date: 18-12-5 下午8:18
"""
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer

from users.models import User


def generate_verify_email_url(user_id):
    """生成激活邮箱的url

    :param user_id: 用户ID
    :return:
    """
    # 加密有效期10分钟
    serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=10 * 60)
    # 获取用户信息
    user = User.objects.get(id=user_id)
    # 封装用户ID和邮箱
    data = {'user_id': user.id, 'email': user.email}
    # 根据封装信息生成token
    token = serializer.dumps(data).decode()
    # 拼接激活邮箱url
    verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token
    # 返回
    return verify_url
