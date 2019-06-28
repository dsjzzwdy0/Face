#-*- coding:utf-8 -*-
import tornado.web
import os
import os.path
from pycket.session import SessionMixin
from models.result_warpper import *
from models.face_info import *
import json
from utils.recognition import *


WIDTH = 128
HEIGHT = 128
IMAGE_FORMAT = '.png'
face_detector = FaceDetector(WIDTH, HEIGHT)
face_recognizer = FaceRecognizer(face_detector)


def get_image_content_type(format):
    if format == '.jpg' or format == 'jpg':
        return 'image/jpeg'
    elif format == '.png' or format == 'png':
        return 'image/png'
    else:
        return 'image/jpeg'


def create_face_info(rawimage, userid, name):
    '''
    创建头像信息数据
    :param rawimage: 原始人脸图像
    :param userid: 用户编号
    :param name: 用户名称
    :return: 人脸对象数据
    '''
    face_img, shape = face_detector.get_normalize_face(rawimage)
    # print(face_img)
    if face_img is None or shape is None:
        return None

    # 人脸特征提取
    face_feature = face_detector.encode_face_feature(face_img)
    if face_feature is None:
        return None;

    face = FaceInfo()
    face.format = IMAGE_FORMAT
    face.userid = userid
    face.name = name
    face.width = shape[0]
    face.height = shape[1]
    face.channel = shape[2]
    face.facebytes = get_face_image_byte(face_img)
    face.features = face_feature
    return face


'''
def create_face_feature(face):
    if face.facebytes is None:
        return None;

    if face.width <= 0 or face.height <= 0 or face.channel <= 0:
        return None;

    # shape = (face.width, face.height, face.channel)
    face_image = cv2_decode_byte_array(face.facebytes)

    # 人脸特征提取
    face_feature = face_detector.encode_face_feature(face_image)
    if face_feature is None:
        return None;

    feature = FeatureInfo()
    feature.faceid = face.id
    feature.userid = face.userid
    feature.features = face_feature             # 人脸特征属性
    return feature
'''


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def initialize(self):
        self.db = dbSession
        # print ("-----------initialize方法---------")

    def on_finish(self):
        self.db.close()
        # print ("-------------on_finish方法----------------")

    def add_model(self, model):
        try:
            self.db.add(model)
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def response_json(self, result):
        self.set_header('Content-type', 'application/json')
        return self.write(json.dumps(result.__dict__))


# 定义处理类型
class IndexHandler(BaseHandler):
    # 添加一个处理get请求方式的方法
    def get(self):
        image = cv2.imread('d:/Python/images/person.jpg')  # 图片路径

        if image is None:
            return self.write('好看的皮囊千篇一律，有趣的灵魂万里挑一。')
        else:
            self.set_header("Content-Type", "image/png")
            bytes = get_cv2_byte_array(image)
            self.write(bytes)


class FaceHandler(BaseHandler):
    def get(self):
        image = Image.open('d:/Python/images/person.jpg')
        self.set_header("Content-Type", "image/png")
        self.write(get_image_byte_array(image))


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
        meta = self.request.files['file'][0]  # 提取表单中‘name’为‘file’的文件元数据
        if meta is None:
            result = failure('There are no image file uploaded, please set the iamge file')
            return self.response_json(result)

        upload_path = os.path.join("d:/index", 'face/tempdir')  # 文件的暂存路径
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

        bytes = meta['body']




class MainHandler(BaseHandler):
    def get(self):
        self.render("index.html", list_info = [11,22,33])


class FaceRecognizeHandler(BaseHandler):
    '''
    人脸识别
    '''
    def get(self):
        self.render("recognize.html")

    def post(self):
        meta = self.request.files['file'][0]

        if meta is None:
            result = failure("Error, there is no image file uploaded.")
            return self.response_json(result)

        bytes = meta['body']
        image = cv2_decode_byte_array(bytes)
        if image is None:
            print("Failure image data")
            result = failure("Failure image data")
            return self.response_json(result)

        # 识别人脸
        feature = face_recognizer.predict(image)
        if feature is None:
            print("Failure to predict the face image.")
            result = failure("Failure to predict the face image.")
            return self.response_json(result)

        data = {}
        data['id'] = feature.id
        data['userid'] = feature.userid
        data['name'] = feature.name
        result = ok_data(data)
        return self.response_json(result)


class FaceRegistHandler(BaseHandler):
    def get(self):
        # user = self.get_query_argument("user", "test")
        # print("User name is", user)
        self.render("regist.html")

    def post(self):
        meta = self.request.files['file'][0]
        userid = self.get_body_argument('userid', '001')
        name = self.get_body_argument('name', 'test01')

        if meta is None:
            result = failure("Error, there is no image file uploaded.")
            return self.response_json(result)
        else:
            bytes = meta['body']
            '''if len(bytes) > 65 * 1024:
                result = failure("Error, the file image is > 65k, can't processed.")
                return self.response_json(result)
            '''
            image = cv2_decode_byte_array(bytes)
            if image is None:
                print("Failure image data")
                result = failure("Failure image data")
                return self.response_json(result)

            face = create_face_info(image, userid, name)
            if face is None:
                print("There are no face detected in the image file")
                result = failure("There are no face detected in the image file")
                return self.response_json(result)

            if self.add_model(face):
                # print('Face {}, {}, {}'.format(face.id, face.userid, face.name))
                # feature = create_face_feature(face)
                # if feature is None or not self.add_model(feature):
                #    print("There are no face detected in the image file or error occured when save feature.")
                #    result = failure("There are no face detected in the image file or error occured when save feature.")
                #    return self.response_json(result)

                # print('Feature {}, {}, {}'.format(feature.id, feature.faceid, feature.userid))
                # face.facebytes = None
                face_recognizer.add_feature(face)        #添加人脸特征数据

                data = {}
                data['id'] = face.id
                data['userid'] = face.userid
                data['name'] = face.name
                result = ok_data(data)
            else:
                result = failure('Error occured when save in database')

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