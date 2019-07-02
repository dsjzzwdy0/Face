# coding=utf-8
from utils import dlib_utils
import cv2
import io
from PIL import Image
import numpy as np
from models.models_def import *
from utils.log import *


def get_cv2_byte_array(image, format='png'):
    '''
    从cv2图像获得字节数组
    :param image: cv2图像数据
    :param format: 图像格式
    :return: 字节数组
    '''
    if image is None:
        return None
    else:
        img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        return get_image_byte_array(img, format)


def get_image_byte_array(image, format='png'):
    '''
    将图像数据(这里是PIL Image格式)转存为字节数组
    :param image: 原始图像数据
    :param format: 图像格式，PNG就是图片格式，我试过换成JPG/jpg都不行
    :return: 字节数据
    '''
    if image is None:
        return None
    else:
        img_byte_arr = io.BytesIO()                     # 创建一个空的Bytes对象
        image.save(img_byte_arr, format=format)         # PNG就是图片格式，我试过换成JPG/jpg都不行
        return img_byte_arr.getvalue()                  # 这个就是保存的图片字节流


def cv2_decode_byte_array(bytes):
    '''
    从客户端POST上来的图像文件进行图像解码
    :param bytes: 图像字节数组数据
    :return: cv2 支持的图像数据
    '''
    image = np.asarray(bytearray(bytes), dtype=np.uint8)     #转换成图像
    image = cv2.imdecode(image, cv2.COLOR_RGBA2BGR)
    return image


def decode_byte_array(bytes, shape):
    '''
    字节数组转成图像
    :param bytes: 字节数组
    :param shape: 形状数据
    :return: 影像数据
    '''
    face_img = np.array(bytearray(bytes), dtype="uint8").reshape(shape[0], shape[1], shape[2])
    return face_img


def get_face_image_byte(face_image):
    '''
    将自动识别出的人脸图像数据转换成图像字节数组
    字节数组的格式为PNG格式
    :param face_image: 识别出的人脸数据 np.ndarray
    :return: 字节数组数据
    '''
    face_img = Image.fromarray(cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB))
    return get_image_byte_array(face_img)


class FaceRecognizer:
    '''
    人脸识别检测类
    '''
    def __init__(self, face=None, tolerance=0.6, width=128, height=128):
        self.width = width
        self.height = height
        self.tolerance = tolerance
        self.face = face
        self.db = dbSession
        self.features = []
        self.know_faces = []
        self.initialize()

    def initialize(self):
        '''
        从数据库中初始化人脸特征库
        :return:
        '''
        logger.info('Initialize known faces from database geoqs(face_info)...')
        feature_infos = self.db.query(FeatureInfo).all()
        size = len(feature_infos)
        logger.info('There are {} know labels and faces in the database.'.format(size))
        for feature_into in feature_infos:
            self.add_feature(feature_into)

    def add_feature(self, feature_info):
        '''
        加入到人脸特征库中
        :param feature_info: 特征数据
        :return: 无
        '''
        if feature_info is None:
            return

        self.features.append(feature_info)
        self.know_faces.append(np.frombuffer(feature_info.features))
        # print('Features: is ')
        # print(np.frombuffer(feature_info.features))

    def remove_feature(self, index):
        '''
        删除某个序号下的元素
        :param index: 序号
        :return: 无
        '''
        if len(self.features) <= index or len(self.know_faces) <= index:
            return
        else:
            del self.features[index]
            del self.know_faces[index]

    def predict(self, unknow_image):
        '''
        检测人脸图像
        :param unknow_image: 未分类的人脸数据
        :return:
        '''
        unknow_feature = self.face.encode_face_feature(unknow_image)
        dist = dlib_utils.face_distance(self.know_faces, unknow_feature)
        # print(dist)

        min_dist = 100000
        index = -1
        for i in range(0, len(dist)):
            if dist[i] < min_dist:
                min_dist = dist[i]
                index = i

        if min_dist < self.tolerance and index > -1:
            return self.features[index]
        return None

    def close(self):
        self.db.close()


class FaceDetector:
    '''
    人脸检测与识别的类
    '''
    def __init__(self, width=128, height=128):
        self.width = width
        self.height = height

    @staticmethod
    def find_face_locations(image):
        '''
        查找人脸所在的图像的位置
        :param image: 图像数据
        :return: 人脸所在图像的位置,位置是一个列表
        '''
        return dlib_utils.face_locations(image)

    def encode_face_feature(self, face_image):
        return dlib_utils.face_encodings(face_image)[0]

    def find_and_draw_face_locations_path(self, image_path):
        '''
        查找并把人脸的图像位置进行标示
        :param image_path: 图像位置
        :return: 标示之后的图像数据
        '''
        image = cv2.imread(image_path)
        if image is None:
            return None
        return self.find_and_draw_face_locations(image)

    def find_and_draw_face_locations(self, image):
        '''
        查找并把人脸图像的位置用方框进行标示
        :param image: 图像数据
        :return: 标示之后的图像
        '''
        locations = FaceDetector.find_face_locations(image)
        size = len(locations)

        if size <= 0:
            return image

        for face_location in locations:
            (top, right, bottom, left) = face_location
            cv2.rectangle(image, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 0), 1)

        return image

    def find_main_face_location(self, image):
        '''
        识别人脸数据，如果一张图片中有多张人脸，则只返回最主要的人脸
        :param image: 包含人脸的图像数据
        :return: 人脸图像
        '''
        face_locations = FaceDetector.find_face_locations(image)
        size = len(face_locations)

        if size <= 0:
            return None

        location = None
        for face_location in face_locations:            #确定最大的人脸图像区域
            if location is None :
                location = face_location
                continue

            (top0, right0, bottom0, left0) = face_location
            (top1, right1, bottom1, left1) = location

            width0 = right0 - left0
            height0 = bottom0 - top0
            width1 = right1 - left1
            height1 = bottom1 - top1

            # 按照确定的面积最大的区域
            if width0 * height0 > width1 * height1:
                location = face_location

        return location

    def get_normalize_face(self, image):
        '''
        获得标准化的人脸图像及人脸尺
        :param image: 包含人脸的图像数据
        :return: 人脸图像数据、图像尺寸数据
        '''
        location = self.find_main_face_location(image)
        if location is not None:
            (top, right, bottom, left) = location
            face_image = image[top:bottom, left:right]
            face_image = cv2.resize(face_image, (self.width, self.height), cv2.INTER_LINEAR)
            return face_image, face_image.shape
        else:
            return None, None