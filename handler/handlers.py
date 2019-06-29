# -*- coding:utf-8 -*-

import tornado.web
import os
import os.path
import json
from datetime import *
from pycket.session import SessionMixin
from models.result_warpper import *
from models.models_def import *
from utils.recognition import *
from utils.file_utils import *
from conf import settings


WIDTH = 128
HEIGHT = 128
IMAGE_FORMAT = '.png'
face_detector = FaceDetector(WIDTH, HEIGHT)
face_recognizer = FaceRecognizer(face_detector)
tmp_path = settings.get_conf()['temp_path']
if str.strip(tmp_path) == '':
    tmp_path = 'd:/index/face/tempdir'                  # 文件存储的路径
file_utils = FileUtils(tmp_path)
print('The server use the path "', tmp_path, '" to store the temp files.')


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


def create_temp_file_info(userid, filename, source):
    filetype = file_extension(filename)
    path = file_utils.get_new_file_path(filetype)

    fileinfo = TempFileInfo()
    fileinfo.userid = userid
    fileinfo.name = filename
    fileinfo.filetype = filetype
    fileinfo.createtime = datetime.now()
    fileinfo.path = path
    fileinfo.source = source
    return fileinfo


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
    '''
    基础处理器，主要实现的功能包括:
    1、初始化数据库链接
    2、通用错误控制页面
    3、数据存储
    4、页面跳转
    5、文件处理
    '''
    def initialize(self):
        self.db = dbSession
        # print ("-----------initialize方法---------")

    def on_finish(self):
        self.db.close()
        # print ("-------------on_finish方法----------------")

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('public/404.html')
        elif status_code == 500:
            self.render('public/500.html')
        else:
            self.write("Gosh darnit, user! You caused a %d error." % status_code)

    def add_model(self, model):
        '''
        向数据库中加入数据记录
        :param model: 数据记录
        :return: 是否成功的标志
        '''
        try:
            self.db.add(model)
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def response_image(self, image, image_type='pil', format='png'):
        '''
        向客户端写出图像数据
        :param image_type: 图像类型
        :param image: 图像数据
        :param format: 图像格式
        :return: 返回写出的值
        '''
        if image_type == 'cv2':
            bytes = get_cv2_byte_array(image, format)
        else:
            bytes = get_image_byte_array(image, format)

        self.set_header("Content-Type", get_image_content_type(format))
        return self.write(bytes)

    def response_json(self, result):
        '''
        向关端返回JSON字符串信息
        :param result: 结果数据
        :return:
        '''
        self.set_header('Content-type', 'application/json')
        return self.write(json.dumps(result.__dict__))

    def save_file_info(self, file_meta, source):
        '''
        保存从客户端提交上来的数据，这里的保存将会有两个同步动作：
        1、在临时文件夹下保存二进制数据文件
        2、在数据库中记录文件的地址及相关信息
        :param file_meta: Post提交上来的文件数据
        :param source: 数据来源，这里指数据接口
        :return: 文件信息
        '''
        file_name = file_meta['filename']
        bytes = file_meta['body']

        if str.strip(file_name) == '' or bytes is None:
            return None

        userid = 'anonymous'
        file_info = create_temp_file_info(userid, file_name, source)
        file_path = file_utils.get_file_path(file_info.path)

        try:
            f = open(file_path, 'wb')
            f.write(bytes)
            f.flush()
            f.close()
        except Exception as e:
            print(e)
            return None

        # print('Save file information ', file_meta['filename'])
        if self.add_model(file_info):
            return file_info
        else:
            return None


# 定义处理类型
class IndexHandler(BaseHandler):
    '''
    首页处理页面，主要功能包括：
    1、系统功能引导：人脸检测、人脸注册、人脸识别三个页面导航
    2、系统管理导航：已经注册和标记的人脸库管理
    '''
    def get(self):
        self.render("index.html", list_info=[11, 22, 33])
        '''
        image = cv2.imread('d:/Python/images/person.jpg')  # 图片路径
        if image is None:
            return self.write('好看的皮囊千篇一律，有趣的灵魂万里挑一。')
        else:
            self.set_header("Content-Type", "image/png")
            bytes = get_cv2_byte_array(image)
            self.write(bytes)
        '''


class FacePictureHandler(BaseHandler):
    '''
    人脸图像快速调用和浏览功能
    通过ID值、图像type类型等参数，系统返回人脸头像数据
    '''
    def get(self):
        id = self.get_query_argument('id')
        if id.strip() == '':
            return self.send_redirect()
        else:
            face = self.db.query(FaceInfo).filter(FaceInfo.id == id).first()
            if face is None:
                return self.send_redirect()
            else:
                format = face.format
                self.set_header("Content-Type", get_image_content_type(format))
                return self.write(face.facebytes)

    def send_redirect(self):
        '''
        系统跳转到某一个固定的图像地址
        :return:
        '''
        return self.redirect('static/images/maps.png')


class FaceDetectPictureHandler(BaseHandler):
    '''
    获得人脸检测的图像数据
    '''
    def get(self):
        try:
            id = self.get_query_argument('id')
        except Exception as e:
            return self.send_redirect()

        tmp_file = self.db.query(TempFileInfo).filter_by(id=id).first()
        if tmp_file is None:
            return self.send_redirect()

        image_path = file_utils.get_file_path(tmp_file.path)
        image = face_detector.find_and_draw_face_locations_path(image_path)
        if image is None:
            return self.send_redirect()

        return self.response_image(image, 'cv2')

    def send_redirect(self):
        '''
        系统跳转到某一个固定的图像地址
        :return:
        '''
        return self.redirect('static/images/maps.png')

class FaceDetectHandler(BaseHandler):
    '''
    人脸检测功能：主要用于测试和试用
    这里将保存被检测的人脸数据
    数据的存储在临时文件夹中，并通过文件库进行索引管理
    '''
    def get(self):
        return self.render('detect.html')

    def post(self):
        meta = self.request.files['file'][0]  # 提取表单中‘name’为‘file’的文件元数据
        if meta is None:
            result = failure('There are no image file uploaded, please set the iamge file')
            return self.response_json(result)

        file_info = self.save_file_info(meta, 'detect')
        if file_info is None:
            result = failure('Error occured when save the image file.')
            return self.response_json(result)

        data = {}
        data['id'] = file_info.id
        data['userid'] = file_info.userid
        data['name'] = file_info.name
        result = ok_data(data)
        return self.response_json(result)


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

        self.save_file_info(meta, 'recog')          #仅仅用于保存数据,无其它的用途

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
        userid = self.get_body_argument('userid', '001')
        name = self.get_body_argument('name', 'test01')
        meta = self.request.files['file'][0]
        if meta is None:
            result = failure("Error, there is no image file uploaded.")
            return self.response_json(result)

        self.save_file_info(meta, 'regist')          #仅仅用于保存数据,无其它的用途

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
        (r'/detect', FaceDetectHandler),            # 人脸检测测试接口
        (r'/regist', FaceRegistHandler),            # 人脸注册接口
        (r'/recognize', FaceRecognizeHandler),      # 人脸识别接口
        (r'/getpic', FacePictureHandler),           # 人脸图像数据页面
        (r'/detectpic', FaceDetectPictureHandler)   # 图像检测出人脸
    ]
    return urls;