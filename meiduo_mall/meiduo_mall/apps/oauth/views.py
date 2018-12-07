from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from oauth.models import OAuthQQUser
from oauth.qq_serializers import QQUserSerializer
from oauth.utils import generate_encrypted_openid


class QQURLView(APIView):
    """提供QQ登录页面网址
    GET /oauth/qq/authorization
    """

    def get(self, request):
        """获取QQ登陆页面网址

        :param request:
        :return:
        """
        # next表示登录成功后要进入的界面
        next_ = request.query_params.get('next')
        # 如果没有跳转页
        if not next_:
            # 默认转转首页
            next_ = ''  # 首页
        # 实例化QQ第三方开放平台
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=next_)
        # 获取QQ登陆网址
        login_url = oauth.get_qq_url()
        # 返回QQ登陆网址
        return Response({'login_url': login_url})


class QQUserView(APIView):
    """用户扫码登录的回调处理
    GET     /oauth/qq/user/
    POST    /oauth/qq/user/
    """

    def get(self, request):
        # 获取请求参数 -- code
        code = request.query_params.get('code')
        # 如果没有code请求参数
        if not code:
            # 返回异常信息
            return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)
        # 创建工具对象 -- 实例化QQ第三方开发平台
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            # 根据code获取QQ服务器access_token -- 提交给QQ服务器, 开发者个人信息和code, 进行验证
            access_token = oauth.get_access_token(code)
            # 根据access_token获取QQ服务器openid -- 提交给QQ服务器 access_token, 证明已通过验证
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            print(e)
            return Response({'message': 'QQ服务异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            # 根据openid获取信息
            oauth_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 如果没有此openid信息, 表示需要此用户需要进行绑定账号, 返回openid进行下一步绑定用户
            # 对openid进行加密, 防修改
            openid = generate_encrypted_openid(openid)
            return Response({'openid': openid})
        else:
            # 获取到openid信息, 返回jwt自动登陆
            # 生成消息体(函数)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            # 生成JWT认证(函数)
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            # 获取openid信息中用户信息
            user = oauth_user.user
            # 根据用户信息生成消息体
            payload = jwt_payload_handler(user)
            # 根据消息体生成JWT认证
            token = jwt_encode_handler(payload)
            # 封装返回信息
            response = Response({
                'token': token,
                'user_id': user.id,
                'username': user.username
            })
            return response

    def post(self, request):
        """绑定openid和美多用户

        :param request:
        :return:
        """
        # 实例化序列化器对象
        serializer = QQUserSerializer(data=request.data)
        # 校验请求参数
        serializer.is_valid(raise_exception=True)
        # 绑定openid和美多用户（添加一条表数据）
        user = serializer.save()

        # 生成JWT返回登陆
        # 生成消息体(函数)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # 生成JWT认证(函数)
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # 根据用户信息生成消息体
        payload = jwt_payload_handler(user)
        # 根据消息体生成JWT认证
        token = jwt_encode_handler(payload)
        # 封装响应
        response = Response({
            'token': token,
            'user_id': user.id,
            'username': user.username
        })
        return response
