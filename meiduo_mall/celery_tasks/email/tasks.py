"""celery执行具体任务 -- 发送短信

date: 18-12-5 下午8:15
"""

# 定义任务
from django.conf import settings
from django.core.mail import send_mail

from celery_tasks.main import celery_app


@celery_app.task(name='send_verify_email')
def send_verify_email(to_email, verify_url):
    """发送邮箱验证邮件

    :param to_email: 收件人邮箱
    :param verify_url: 验证邮箱url
    :return: 执行结果
    """
    # 标题
    subject = "美多商城邮箱验证"
    # html样式正文
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' \
                   % (to_email, verify_url, verify_url)
    # 调用Django提供的发送邮件(标题, 普通中文, 发送者, [收件人1, 收件人2...], html正文) -- html正文会代替普通正文
    send_mail(subject, "这是普通正文", settings.EMAIL_FROM, [to_email], html_message=html_message)
    #
    print('发送邮箱验证邮件:', verify_url)
