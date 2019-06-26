# coding=utf-8
import face_recognition
import cv2
import numpy as np
from models import dbSession
from models.face_info import FaceInfo


class FaceRecognizer:
    '''
    人脸识别检测类
    '''
    def __init__(self, width=128, height=128):
        self.width = width
        self.height = height
        self.face = Face(width, height)
        self.db = dbSession
        self.faces = dict()
        self.initialize()

    def initialize(self):
        print('初始化人脸识别程序')
        face_infos = self.db.query(FaceInfo).all()
        for face_info in face_infos:
            print("标识号：", face_info.id)
            self.faces[face_info.id] = face_info

    def add_face(self, face_info):
        pass



class Face:
    '''
    人脸检测与识别的类
    '''
    def __init__(self, width=128, height=128):
        self.width = width
        self.height = height

    @staticmethod
    def find_face_locations(image):
        return face_recognition.face_locations(image)

    def find_main_face_location(self, image):
        face_locations = Face.find_face_locations(image)
        size = len(face_locations)

        if size <= 0:
            return None

        location = None
        for face_location in face_locations:
            if location is None :
                location = face_location
                continue

            (top0, right0, bottom0, left0) = face_location
            (top1, right1, bottom1, left1) = location

            width0 = right0 - left0
            height0 = bottom0 - top0
            width1 = right1 - left1
            height1 = bottom1 - top1

            if width0 * height0 > width1 * height1:
                location = face_location

        return location

    def get_normalize_face(self, image):
        location = self.find_main_face_location(image)
        if location is not None:
            (top, right, bottom, left) = location
            face_image = image[top:bottom, left:right]
            face_image = cv2.resize(face_image, (self.width, self.height), cv2.INTER_LINEAR)
            return face_image
        else:
            return None