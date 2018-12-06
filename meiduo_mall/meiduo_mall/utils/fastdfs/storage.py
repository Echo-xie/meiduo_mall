"""自定义文件存储系统 -- admin站点上传图片保存地址

date: 18-12-6 下午8:28
"""
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from fdfs_client.client import Fdfs_client


class FdfsStorage(FileSystemStorage):
    """自定义文件存储系统类
    FileSystemStorage 实现子类, 重写保存方法
    """

    def _save(self, name, content):
        """重写 -- 保存
        当用户通过django管理后台上传文件时,调用此方法保存文件到FastDFS服务器中
        :param name: 传入的文件名
        :param content: 文件内容
        :return: 上传文件的路径
        """
        # 自定义存储：保存文件到FastDFS服务器
        # 实例化fdfs, 根据配置文件
        client = Fdfs_client('meiduo_mall/utils/fastdfs/client.conf')
        # 读取文件二进制
        dict_data = client.upload_by_buffer(content.read())
        # 如果上传不成功
        if 'Upload successed.' != dict_data.get('Status'):
            # 抛出异常
            raise Exception('上传文件到FastDFS失败')

        # 上传成功, 保存返回文件ID以便保存数据库
        path = dict_data.get('Remote file_id')
        # 返回文件ID -- 也是文件的路径
        return path

    # 重写父类的url函数
    def url(self, name):
        """
        返回文件的完整URL路径
        :param name: 数据库中保存的文件名，类似：
                     group1/M00/00/00/wKjSoFu-wD2AZQ6ZAAERuQ5dzms593.png
        :return: 完整的URL
        """
        return settings.FDFS_URL + name
