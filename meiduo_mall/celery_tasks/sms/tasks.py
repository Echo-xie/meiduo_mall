"""celery执行具体任务 -- 发送短信

date: 18-12-1 下午8:41
"""
from celery_tasks.main import celery_app
from meiduo_mall.libs.yuntongxun.sms import CCP


# 定义任务
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    """发送短信验证码

    :param mobile: 手机号码
    :param sms_code: 短信验证码
    :return: 执行结果
    """
    # CCP().send_template_sms(mobile, [sms_code, 5], 1)
    print('发送短信验证码:', sms_code)
