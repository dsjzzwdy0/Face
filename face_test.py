# coding=utf-8
from utils.recognition import FaceDetector
import cv2
import numpy as np
from utils import recognition
import face_recognition
from PIL import Image
import matplotlib.pyplot as plt
import time
from utils.file_utils import *


def test_for_dir():
    file = FileUtils("d:/index/tempdir")
    path = file.get_new_file_path(".txt")
    print(path)

def test_for_face_database():
    recognition.FaceRecognizer()


def test_for_face_find():
    image_path = "images/trump2.png"
    image = cv2.imread(image_path)

    '''cv2.imshow("Faces", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''

    face = FaceDetector()
    face_img, shape = face.get_normalize_face(image)

    '''cv2.imshow("Faces", face_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''

    # face_img = Image.fromarray(cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB))
    '''plt.figure("dog")
    plt.imshow(face_img)
    plt.show()'''

    start = time.time()
    feature_list = face_recognition.face_encodings(face_img)
    feature0 = feature_list[0]
    end = time.time()
    print('Encode face feature spend time is', (end - start))

    '''
    print(feature0)
    print ('Feature type is ', type(feature0))
    shape = feature0.shape
    print('Feature shape is ', shape)
    bytes = feature0.tobytes()

    feature1 = np.frombuffer(bytes)
    print(feature1)
    '''

    start = time.time()
    feature_list = face_recognition.face_encodings(face_img)
    feature0 = feature_list[0]
    end = time.time()
    print('Encode face feature spend time is', (end - start))


    '''image_path = "images/trump2.png"
    print("test for face find: ", image_path)
    image = cv2.imread(image_path)

    feature0 = face_recognition.face_encodings(image)[0]
    print(feature0)

    image_path = "images/trump.jpg"
    image = cv2.imread(image_path)
    feature1 = face_recognition.face_encodings(image)[0]


    face = Face()
    face_img, shape = face.get_normalize_face(image)
    # print(face_img)

    face_img = cv2.imread('images/trump4.jpg')
    feature = face_recognition.face_encodings(face_img)[0]
    print(feature)

    if face_img is not None:
        cv2.imshow("Faces", face_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    known_faces = [
        feature0,
        feature1
    ]

    results = face_recognition.compare_faces(known_faces, feature)

    print(results)
    '''

    '''
    width = shape[0]
    height = shape[1]
    channel = shape[2]
    print('shape', shape, width, height, channel)
    bytes = bytearray(face_img)
    # print(bytes)

    face_img = np.array(bytearray(bytes), dtype="uint8").reshape(width, height, channel)
    # print (face_img)
    # face_img = recognition.cv2_decode_byte_array(bytes)

    if face_img is not None:
        cv2.imshow("Faces", face_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print ("There are no face found in image file")

    
    face_location = face.find_main_face_location(image)
    #face_image = None

    if face_location is not None:
        # for face_location in face_locations:
            # Print the location of each face in this image
        (top, right, bottom, left) = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
        print("I Found one main faces width: {}, height: {}".format(right - left, bottom - top))
        face_image = image[top:bottom, left:right]
        #cv2.rectangle(face_image, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 0), 1)

        cv2.imshow("Faces", face_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    '''

def main():
    # test_for_face_recognition()
    # test_for_face_find()
    # test_for_face_database()
    test_for_dir()



if __name__ == '__main__':
    # tf.app.run()
    main()