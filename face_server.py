#-*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import os
import json
import cv2
import numpy as np
from conf import settings


#定义处理类型
class IndexHandler(tornado.web.RequestHandler):
    #添加一个处理get请求方式的方法
    def get(self):
        #向响应中，添加数据
        self.write('好看的皮囊千篇一律，有趣的灵魂万里挑一。')


class FaceDetectHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('please upload a image url')

    def post(self):
        upload_path = os.path.join("d:/index", 'files')  # 文件的暂存路径
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

        file_metas = self.request.files['file']  # 提取表单中‘name’为‘file’的文件元数据
        userid = self.get_query_argument("userid", "test")
        name = self.get_query_argument("name", "test")
        print("userid: ", userid, ", name: ", name)

        for meta in file_metas:
            filename = meta['filename']
            print(filename)
            filepath = os.path.join(upload_path, filename)
            bytes = meta['body']
            image = np.asarray(bytearray(bytes), dtype="uint8")
            image = cv2.imdecode(image, 0)
            sp = image.shape
            channel = image.channels
            print("图像长度:", sp[0], ", ", sp[1], ", Channel: ", channel)

            with open(filepath, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                up.write(meta['body'])
            self.write('finished!')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", list_info = [11,22,33])


class RegistHandler(tornado.web.RequestHandler):
    def get(self):
        user = self.get_query_argument("user", "test")
        print("User name is", user)
        self.render("regist.html")

'''
class JsonHandler(tornado.web.RequestHandler):
    def get(self):
        pythonStr = {}
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        student = Student()
        json_str = json.dumps(student.__dict__)
        self.finish(json_str)
'''

if __name__ == '__main__':
    current_path = os.path.dirname(__file__)  # 上一层目录

    urls = [(r'/',IndexHandler),
         (r'/index', MainHandler),
         # (r'/json', JsonHandler),
         (r'/detect', FaceDetectHandler),
         (r'/regist', RegistHandler)]

    #创建一个应用对象
    app = tornado.web.Application(
        urls,
        static_path = os.path.join(current_path, "static"),
        template_path=os.path.join(current_path, 'templates'),  # 配置模板路径
    )

    print('Start server at port ', settings.conf['port'])

    #绑定一个监听端口
    app.listen(settings.conf['port'])
    #启动web程序，开始监听端口的连接
    tornado.ioloop.IOLoop.current().start()