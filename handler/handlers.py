#-*- coding:utf-8 -*-
import tornado.web
import os
from pycket.session import SessionMixin
from models.result_warpper import *
import json
from PIL import Image
from utils.recognition import *


def get_image_content_type(format):
    if format == '.jpg' or format == 'jpg':
        return 'image/jpeg'
    elif format == '.png' or format == 'png':
        return 'image/png'
    else:
        return 'image/jpeg'


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def initialize(self):
        self.db = dbSession
        print ("-----------initialize方法---------")

    def on_finish(self):
        self.db.close()
        # print ("-------------on_finish方法----------------")

    def response_json(self, result):
        self.set_header('Content-type', 'application/json')
        return self.write(json.dumps(result.__dict__))


# 定义处理类型
class IndexHandler(BaseHandler):
    # 添加一个处理get请求方式的方法
    def get(self):
        self.set_header("Content-Type", "image/png")
        imagepath = os.path.join('d:/Python/images/maps.png')  # 图片路径
        with open(imagepath, 'rb') as f:
            image_data = f.read()

        # self.write('好看的皮囊千篇一律，有趣的灵魂万里挑一。')
        self.write(image_data)


class FaceHandler(BaseHandler):
    def get(self):
        image = Image.open('d:/Python/images/maps.png')
        self.set_header("Content-Type", "image/png")
        self.write(get_byte_array(image))


class FacePicture(BaseHandler):
    def get(self):
        id = self.get_query_argument('id')
        # print('Query id value=', id)
        if id.strip() == '':
            return self.send_redirect()
        else:
            face = self.db.query(FaceInfo).filter(FaceInfo.id == id).first()
            if face == None:
                return self.send_redirect()
            else:
                format = face.format
                self.set_header("Content-Type", get_image_content_type(format))
                self.write(face.facebytes)

    def send_redirect(self):
        return self.redirect('static/images/maps.png')


class FaceDetectHandler(BaseHandler):
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


class MainHandler(BaseHandler):
    def get(self):
        self.render("index.html", list_info = [11,22,33])


class FaceRecognizeHandler(BaseHandler):
    '''
    人脸识别类
    '''
    def initialize(self):
        BaseHandler.initialize(self)
        print('初始化方法')
        print ('initialize the face recognize handler.')

    def get(self):
        self.render("recognize.html")

    def post(self):
        meta = self.request.files['file'][0]


class FaceRegistHandler(BaseHandler):
    def get(self):
        # user = self.get_query_argument("user", "test")
        # print("User name is", user)
        self.render("regist.html")

    def post(self):
        meta = self.request.files['file'][0]
        userid = self.get_body_argument('userid', '001')
        name = self.get_body_argument('name', 'test01')

        if meta == None:
            result = failure("Error, there is no image file uploaded.")
            return self.response_json(result)
        else:
            # filename = meta['filename']
            bytes = meta['body']
            if  len(bytes) > 65 * 1024:
                result = failure("Error, the file image is > 65k, can't processed.")
                return self.response_json(result)

            format = '.png'
            face = FaceInfo()
            face.format = format
            face.userid = userid
            face.name = name
            face.facebytes = bytes

            self.db.add(face)
            self.db.commit()

            # face.facebytes = None
            data = {}
            data['id'] = face.id
            data['userid'] = face.userid
            data['name'] = face.name
            result = ok_data(data)
            return self.response_json(result)

def create_urls():
    urls = [
        (r'/', IndexHandler),                       # 首页面
        (r'/index', MainHandler),                   #
        (r'/detect', FaceDetectHandler),            # 人脸检测测试接口
        (r'/regist', FaceRegistHandler),            # 人脸注册接口
        (r'/recognize', FaceRecognizeHandler),      # 人脸识别接口
        (r'/getpic', FacePicture),                  # 人脸图像数据页面
        (r'/face', FaceHandler)
    ]
    return urls;