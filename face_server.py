#-*- coding:utf-8 -*-
import tornado.options
from tornado.options import define, options
import tornado.ioloop
import os
from conf import settings
from handler import handlers

from models import engine
from models.models_def import Base

define("tables", default=False, group="application", help="creat tables", type=bool)

#将创建好的User类，映射到数据库的users表中

def run_database():
    print ('------------create_all-------------')
    Base.metadata.create_all(engine)
    print ('------------create_end-------------')


def init_tornado_app():
    '''
    初始化tornado服务器应用
    :return: app
    '''

    if(options.tables):
        run_database()

    current_path = os.path.dirname(__file__)                    # 上一层目录
    static_path = os.path.join(current_path, "static")          # 静态资源目录
    template_path = os.path.join(current_path, 'templates')     # 配置模板路径
    urls = handlers.create_urls()

    conf = settings.get_conf()
    port = conf['port']

    # 创建一个应用对象
    app = tornado.web.Application(
        handlers = urls,
        static_path = static_path,
        template_path = template_path
    )

    print('Start server listening at port ', port)
    # 绑定一个监听端口
    app.listen(port)
    return app


if __name__ == '__main__':
    init_tornado_app()

    #启动web程序，开始监听端口的连接
    tornado.ioloop.IOLoop.current().start()