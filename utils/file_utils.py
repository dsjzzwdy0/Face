# coding=utf-8
import os.path
import uuid
import time


def file_extension(path):
    return os.path.splitext(path)[1]


class FileUtils:
    def __init__(self, tmp_dir):
        '''
        创建临时文件管理类
        :param tmp_dir: 临时文件路径
        '''
        self.path = tmp_dir

    def get_new_file_path(self, ext):
        '''
        获得一个新的临时文件地址，这里只返回相对路径
        :param ext: 文件扩展名
        :return: 文件相对路径
        '''
        uuid_str = uuid.uuid1()
        now = time.time()
        year = time.strftime('%Y', time.localtime(now))     # 系统当前时间年份
        month = time.strftime('%m', time.localtime(now))    # 月份
        day = time.strftime('%d', time.localtime(now))      # 日期

        file_path = year  + '/' + month + '/' + day + '/'

        temp_path = os.path.join(self.path, file_path)
        if not os.path.exists(temp_path):
            # print("make dirs:", file_path)
            os.makedirs(temp_path)

        return file_path + str(uuid_str) + ext

    def get_file_path(self, relative_path):
        '''
        获得文件的绝对路径
        :param relative_path: 相对路径地址
        :return: 文件绝对路径
        '''
        return os.path.join(self.path, relative_path)