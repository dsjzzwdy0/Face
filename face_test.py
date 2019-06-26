# coding=utf-8
from utils.recognition import Face
import cv2
from utils import  recognition

def test_for_face_database():
    recognition.FaceRecognizer()


def test_for_face_find():
    image_path = "images/person.jpg"
    print("test for face find: ", image_path)
    image = cv2.imread(image_path)
    face = Face()

    face_img = face.get_normalize_face(image)
    if face_img is not None:
        cv2.imshow("Faces", face_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print ("There are no face found in image file")

    '''
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
    test_for_face_database()


if __name__ == '__main__':
    # tf.app.run()
    main()