"""
Model and code was referenced from this repo 
-> https://github.com/atulapra/Emotion-detection/tree/master
"""
import cv2
import keras
import os
import time

import numpy as np

from keras import layers

class Vision:
    def __init__(self) -> None:
        """
        ### Class Summary
        Vision module for processing facial expression through the
        PyschTrackers webcam. A button should trigger an interrupt
        and call the "process" method.

        ---
        ### Parameters
        None

        ---
        ### Return
        Void
        """
        # one hot encode emotions
        self.emotions: dict[int, str] = {
            0: "Angry", 1: "Disgusted", 2: "Fearful", 
            3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"
        }
        # load face detector model
        self.classifier = cv2.CascadeClassifier(
            os.path.join(os.getcwd(),
            'haarcascade_frontalface_default.xml'))
        # recreate model from training.py script
        self.model = keras.models.Sequential(
            [
                # input layer
                layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)),

                # layer 1
                layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Dropout(0.25),

                # layer 2
                layers.Conv2D(128, kernel_size=(3, 3), activation='relu'),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Conv2D(128, kernel_size=(3, 3), activation='relu'),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Dropout(0.25),

                # layer 3
                layers.Flatten(),
                layers.Dense(1024, activation='relu'),
                layers.Dropout(0.5),

                # output layer
                layers.Dense(7, activation='softmax')
            ]
        )
        self.model.load_weights(os.path.join(os.getcwd(), 'model.h5'))

    def process(self, video_idx: int = 0) -> str:
        """
        ### Function Summary
        Processes the current frame of the selected capture device through
        the facial recognition model and then returns the detected emotion.
        
        This is meant to be paired with a button pushing mechanism.

        ---
        ### Parameters
        - video_idx (int, optional): Index of the capture device you want to use. 
        Defaults to 0.
        
        ---
        ### Return
        Returns a string of the detected emotion.
        """
        cap = cv2.VideoCapture(video_idx)  # begin camera feed
        time.sleep(0.5)  # sleep for half a second for loading the webcam
        ret, frame = cap.read()  # read success bool and frame
        if not ret:  # if ret is false, no frame was processed, so raise an error
            raise Exception(f"No frame was available to captured from device at index {video_idx}")
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert frame to greyscale
        faces = self.classifier.detectMultiScale(grey, scaleFactor=1.3, minNeighbors=5)  # detect faces
        x, y, w, h =  faces[0]  # get the first face detected (there should only be one face in the camera)
        aoi = grey[y:y + h, x:x + w]  # get area of interest/specific face
        # crop the image for inputting in the facial expression model
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(aoi, (48, 48)), -1), 0)
        prediction = self.model.predict(cropped_img)  # predict emotions
        # get the index of the emotion with the highest probability of being correct
        idx = int(np.argmax(prediction))
        cap.release()  # release camera feed
        # print(self.emotions[idx])
        return self.emotions[idx]

    def process_live(self, video_idx: int = 0) -> None:
        """
        ### Function Summary
        Displays a live feed with the facial recognition model 
        processed results.

        ---
        ### Parameters
        - video_idx (int, optional): Index of the capture device you want to use. 
        Defaults to 0.
        
        ---
        ### Return
        Void. A window displaying camera feed and a bounding box around a face
        with an emotion label at the bottom.
        """
        cap = cv2.VideoCapture(video_idx)  # begin camera feed
        while True:
            ret, frame = cap.read()  # read success bool and frame
            if not ret:  # if ret is false, no frame was processed, so raise an error
                raise Exception(f"No frame was available to captured from device at index {video_idx}")
            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert frame to greyscale
            faces = self.classifier.detectMultiScale(grey, scaleFactor=1.3, minNeighbors=5)  # detect faces
            for (x, y, w, h) in faces:  # loop over detected face positions
                cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)  # draw a rectangle
                aoi = grey[y:y + h, x:x + w]  # get area of interest/specific face
                # crop the image for inputting in the facial expression model
                cropped_img = np.expand_dims(np.expand_dims(cv2.resize(aoi, (48, 48)), -1), 0)
                prediction = self.model.predict(cropped_img)  # predict emotions
                # get the index of the emotion with the highest probability of being correct
                idx = int(np.argmax(prediction))
                # draw the predicted emotion to the frame
                cv2.putText(
                    frame, self.emotions[idx], (x+20, y-60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            # display the frame onto a window
            cv2.imshow('PsychTracker', cv2.resize(frame, (1600, 960), interpolation = cv2.INTER_CUBIC))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # release camera and destroy all opencv windows
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    vis = Vision()
    vis.process()