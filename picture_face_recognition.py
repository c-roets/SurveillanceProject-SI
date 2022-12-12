import face_recognition
import cv2
import numpy as np

def face_recognition_app(picture):
    # This is a super simple (but slow) example of running face recognition on live video from your webcam.
    # There's a second example that's a little more complicated but runs faster.

    # PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
    # OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
    # specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

    # Get a reference to webcam #0 (the default one)
    #video_capture = cv2.VideoCapture(0)

    # Load a sample picture and learn how to recognize it.
    jonas_image = face_recognition.load_image_file("jonas.jpg")
    jonas_face_encoding = face_recognition.face_encodings(jonas_image)[0]

    # Load a second sample picture and learn how to recognize it.
    calvin_image = face_recognition.load_image_file("calvin.jpg")
    calvin_face_encoding = face_recognition.face_encodings(calvin_image)[0]
    
    auke_image = face_recognition.load_image_file("auke.jpg")
    auke_face_encoding = face_recognition.face_encodings(auke_image)[0]
    
    glenn_image = face_recognition.load_image_file("glenn.jpg")
    glenn_face_encoding = face_recognition.face_encodings(glenn_image)[0]
    
    thibo_image = face_recognition.load_image_file("thibo.jpg")
    thibo_face_encoding = face_recognition.face_encodings(thibo_image)[0]
    
    


    #third picture
    #auke_image = face_recognition.load_image_file("auke.jpg")
    #auke_face_encoding = face_recognition.face_encodings(auke_image)[0]




    # Create arrays of known face encodings and their names
    known_face_encodings = [
        jonas_face_encoding,
        calvin_face_encoding,
        auke_face_encoding,
        glenn_face_encoding
    ]
    known_face_names = [
        "Jonas",
        "Calvin",
        "Auke",
        "Glenn",
        "thibo"
    ]

    # Grab a single frame of video
    img = face_recognition.load_image_file(picture)
    # Convert the image from BGR color (which OpenCV uses) to RGB cqqolor (which face_recognition uses)
    rgb_frame = img[:, :, ::-1]

    # Find all the faces and face enqcodings in the frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # Draw a box around the face
        #cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)           fit rectangle around face

        # Draw a label with a name below the face
        #cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        #font = cv2.FONT_HERSHEY_DUPLEX
        #cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    #cv2.imshow('Video', img)

    # Hit 'q' on the keyboard to quit!
    #if cv2.waitKey(10000) & 0xFF == ord('q'):
        #break
    return name
wie = face_recognition_app("jonas2.jpg")   #test
print(wie)
    # Release handle to the webcam
    #video_capture.release()
    #cv2.destroyAllWindows()