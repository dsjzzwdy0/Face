# coding=utf-8
import os.path
import uuid
import time

def file_extension(path):
    return os.path.splitext(path)[1]


class FileUtils:
    def __init__(self, tmp_dir):
        self.path = tmp_dir

    def get_new_file_path(self, ext):
        uuid_str = uuid.uuid1()
        now = time.time()
        year = time.strftime('%Y', time.localtime(now))     # 系统当前时间年份
        month = time.strftime('%m', time.localtime(now))    # 月份
        day = time.strftime('%d', time.localtime(now))      # 日期

        file_path = self.path + '/upload_files/' + year  + '/' + month + '/' + day
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        return os.path.join(file_path, str(uuid_str) + ext)

        '''
        if not os.path.exists(file_year):
            os.mkdir(file_year)
            os.mkdir(file_month)
            os.mkdir(file_day)
        else:
            if not os.path.exists(file_month):
                os.mkdir(file_month)
                os.mkdir(file_day)
            else:
                if not os.path.exists(file_day):
                    os.mkdir(file_day)
        '''