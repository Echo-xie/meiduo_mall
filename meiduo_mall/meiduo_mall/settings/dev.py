"""
Django settings for DjangoDemo project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import datetime
import os
import sys

# 当前工程根目录
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 修改导包路径
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# 项目加密秘钥
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pqbltcuwumr#yoqlry4^fleh)hfidhn*v-p2hcwjpx72u1s(f!'

# 调试模式
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 允许访问路径 -- 调试模式关闭后
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "api.lnsist.top",
]

# Application definition

# 注册子应用
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 第三方库
    "rest_framework",  # DRF
    "corsheaders",  # 跨域请求
    # 自定义子应用
    "users.apps.UsersConfig",
    "verifications.apps.VerificationsConfig",
    "oauth.apps.OauthConfig",
]

# 中间层列表
MIDDLEWARE = [
    # 安全过滤
    'django.middleware.security.SecurityMiddleware',
    # session
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 公共中间件
    'django.middleware.common.CommonMiddleware',
    # csrf防护
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 验证中间件
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 返回信息中间件
    'django.contrib.messages.middleware.MessageMiddleware',
    # 框架扩展中间件
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 跨域请求
    'corsheaders.middleware.CorsMiddleware',
]

# 根路由路径
ROOT_URLCONF = 'meiduo_mall.urls'

# 设置模板路由配置
TEMPLATES = [
    {
        # 模板解析引擎
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 模板文件保存目录
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        # 是否可以添加目录
        'APP_DIRS': True,
        # 选项
        'OPTIONS': {
            # 模板中使用的扩展包选项
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# wsgi应用基类
WSGI_APPLICATION = 'meiduo_mall.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# 数据库配置
DATABASES = {
    'default': {
        # 数据库引擎
        'ENGINE': 'django.db.backends.mysql',
        # 数据库主机ip
        'HOST': '127.0.0.1',
        # 数据库端口
        'PORT': 3306,
        # 数据库用户名
        'USER': 'root',
        # 数据库用户密码
        'PASSWORD': '123456',
        # 数据库名字
        'NAME': 'db_meiduo_mall',
        # 指定测试数据库的字符集
        'TEST_CHARSET': "utf8",
        # 排序规则
        'TEST_COLLATION': "utf8_general_ci",
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

# 密码验证
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# 本地化语言
# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'  # 中文

# 本地化时区
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'  # 上海

# 国际化
USE_I18N = True

# 国际化
USE_L10N = True

# 是否自动转换时区
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# 访问静态文件的URL前缀
STATIC_URL = '/static/'

# 存放查找静态文件的目录 -- 仅在调试模式下（DEBUG=True）能对外提供静态文件。
STATICFILES_DIRS = [
    # 根据当前目录路径拼接地址
    os.path.join(BASE_DIR, 'static_files'),
]
# 上传文件保存路径
MEDIA_ROOT = os.path.join(BASE_DIR, "static_files/media")

# 缓存
CACHES = {
    # 规则名称
    "default": {
        # 数据库终端
        "BACKEND": "django_redis.cache.RedisCache",
        # 数据库地址 -- 密码
        "LOCATION": "redis://:123456@127.0.0.1:6379/0",
        # 选项
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 保存session
    "session": {
        # 数据库终端
        "BACKEND": "django_redis.cache.RedisCache",
        # 数据库地址 -- 密码
        "LOCATION": "redis://:123456@127.0.0.1:6379/14",
        # 选项],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 保存短信验证码
    "sms_codes": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:123456@127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
# session引擎
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# 缓存规则
SESSION_CACHE_ALIAS = "session"

# 日志文件配置
LOGGING = {
    # 版本
    'version': 1,
    # 是否禁用已经存在的日志器
    'disable_existing_loggers': False,
    # 日志信息显示的格式
    'formatters': {
        # 详情
        'verbose': {
            # 格式 "日志等级 时间 类型 行号 信息"
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        # 简单
        'simple': {
            # 格式 "日至登记 类型 行号 信息"
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        # django在debug模式下才输出日志
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 日志处理方法
    'handlers': {
        # 向终端中输出日志
        'console': {
            # 日志等级
            'level': 'INFO',
            # 参数 -- 只在debug模式下生效
            'filters': ['require_debug_true'],
            # 处理类
            'class': 'logging.StreamHandler',
            # 输出格式
            'formatter': 'simple'
        },
        # 向文件中输出日志
        'file': {
            # 日志等级
            'level': 'INFO',
            # 处理类
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志文件的位置
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/meiduo.log"),
            # 日志文件的最大容量
            'maxBytes': 300 * 1024 * 1024,
            # 日志文件数量  300M * 10
            'backupCount': 10,
            # 输出格式
            'formatter': 'verbose'
        },
    },
    'loggers': {
        # 定义了一个名为django的日志器
        'django': {
            # 可以同时向终端与文件中输出日志
            'handlers': ['console', 'file'],
            # 日志器接收的最低日志级别
            'level': 'INFO',
        },
    }
}

# 建议：项目开发完成再添加进来
# DRF相关配置
REST_FRAMEWORK = {
    # 开启自定义捕获未处理异常
    # 'EXCEPTION_HANDLER': 'meiduo_mall.utils.exceptions.custom_exception_handler',
    # 配置默认验证方式
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # jwt认证
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 管理后台使用
        'rest_framework.authentication.SessionAuthentication',
        # 基本认证
        'rest_framework.authentication.BasicAuthentication',
    ),
}
# jwt认证配置
JWT_AUTH = {  # 导包： import datetime
    # jwt有效时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 修改登录成功接口返回的响应参数, 新增 user_id 和 username两个字段
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'verifications.utils.jwt_response_payload_handler',
}
# 扩展登录接口: 使用自定义的认证后台, 使之支持可以使用用户名或手机号登录
AUTHENTICATION_BACKENDS = [
    'verifications.utils.UsernameMobileAuthBackend',
]
# 指定可以跨域访问当前服务器(127.0.0.1:8000)的白名单
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8080',
    'localhost:8080',
    'www.lnsist.top:8080',
    'api.lnsist.top:8000',
    'www.meiduo.site:8080',
    'api.meiduo.site:8000',
)
# 指定在跨域访问中，后台是否支持cookie操作
CORS_ALLOW_CREDENTIALS = True
# 在项目配置文件中，指定使用自定义的用户模型类
AUTH_USER_MODEL = 'users.User'
# QQ开放平台配置
# APP ID
QQ_CLIENT_ID = '101474184'
# APP Key
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
# 登录成功的回调地址
# QQ_REDIRECT_URI = 'http://www.lnsist.top:8080/oauth_callback.html'
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'