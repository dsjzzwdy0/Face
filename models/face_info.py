# coding=utf-8

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, BLOB, DateTime, ForeignKey
from models import engine
from models import dbSession

Base = declarative_base(engine)

# 定义好一些属性，与user表中的字段进行映射，并且这个属性要属于某个类型

class FaceInfo(Base):
    __tablename__ = 'face_info'
    id = Column(Integer, primary_key=True)
    userid = Column(String(30))
    name = Column(String(32))
    format = Column(String(10))
    facebytes = Column(BLOB)

    # 可以在类里面写别的方法,类似查询方法
    @classmethod
    def all(cls):
        return dbSession.query(cls).all()