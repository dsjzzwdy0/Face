# -*- coding:utf-8 -*-
import os
from conf import *
from configparser import  ConfigParser
from utils.log import *


conf_file = os.path.join(path, 'conf/conf.ini')
conf = dict()


def get_conf():
    size = len(conf)
    if size <= 0:
        # conf_file = os.path.join()
        logger.info('Load configuration file: ' + conf_file)
        config = ConfigParser()
        config.read(conf_file, encoding='utf_8')
        # print(config.items('db'))
        # print ('Read server configuration information...')

        conf.update(config.items('db'))
        # config.dict(conf)
        # conf['port'] = 8000
    return conf
