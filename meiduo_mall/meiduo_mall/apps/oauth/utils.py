"""第三方开发平台工具

date: 18-12-5 下午6:53
"""
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer, BadData


def generate_encrypted_openid(openid):
    """对openid进行加密

    :param openid: 用户的openid
    """
    # 有效期10分钟
    serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=600)
    return serializer.dumps({'openid': openid}).decode()


def check_encrypted_openid(encrypted_openid):
    """校验openid是否过期,是否被篡改

    :param encrypted_openid: 加密的openid
    :return: openid or None
    """
    # 有效期10分钟
    serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=600)
    try:
        # 解密
        data = serializer.loads(encrypted_openid)
    except BadData:
        return None
    else:
        return data.get('openid')
