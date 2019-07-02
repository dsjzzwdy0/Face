#!/usr/bin/env python


# encoding: utf-8

#引入基本的包

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from conf import settings
import pymysql


# 连接数据库的数据
conf = settings.get_conf()

HOSTNAME = conf['server']
DBPORT = conf['dbport']
DATABASE = conf["dbname"]
USERNAME = conf['user']
PASSWORD = conf['password']

# DB_URI的格式：dialect（mysql/sqlite）+driver://username:password@host:port/database?charset=utf8
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, DBPORT, DATABASE)


# 创建引擎
engine = create_engine(DB_URI, echo=False, pool_recycle=3600)

# sessionmaker生成一个session类
Session = sessionmaker(bind=engine)
dbSession = Session()