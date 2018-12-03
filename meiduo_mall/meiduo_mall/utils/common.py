"""通用工具

date: 18-12-3 下午4:07
"""
from django_redis import get_redis_connection


def get_sms_code_by_mobile(mobile):
    """根据手机号码获取对应验证码

    :param mobile: 手机号码
    :return: 转码后的验证码
    """
    # 访问配置信息, 获取数据库连接
    redis_conn = get_redis_connection('sms_codes')
    # 获取此手机号码在数据库中的数据
    real_sms_code = redis_conn.get('sms_%s' % mobile).decode()
    # 返回转码后手机对应验证码
    return real_sms_code
