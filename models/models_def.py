# coding=utf-8

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, BLOB, DateTime, ForeignKey
from models import engine
from models import dbSession

Base = declarative_base(engine)


class FeatureInfo(Base):
    __tablename__ = 'face_info'
    id = Column(Integer, primary_key=True)
    userid = Column(String(30))
    name = Column(String(32))
    features = Column(BLOB)


# 定义好一些属性，与user表中的字段进行映射，并且这个属性要属于某个类型
class FaceInfo(FeatureInfo):
    format = Column(String(10))
    width = Column(Integer)
    height = Column(Integer)
    channel = Column(Integer)
    facebytes = Column(BLOB)
    # thumbnail = Column(BLOB)

    # 可以在类里面写别的方法,类似查询方法
    @classmethod
    def all(cls):
        return dbSession.query(cls).all()


class TempFileInfo(Base):
    __tablename__ = 'tmp_file_info'
    id = Column(Integer, primary_key=True)              # ID编号
    name = Column(String(50))                           # 文件名字
    filetype = Column(String(10))                       # 文件类型
    path = Column(String(200))                          # 文件路径，这里是存储相对路径
    userid = Column(String(30))                         # 用户编号
    createtime = Column(DateTime)                       # 创建时间
    # thumbnail = Column(BLOB)                          # 缩略图
    source = Column(String(10))                         # 数据来源：图像检测、图像注册