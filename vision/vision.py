"""
Model and code was referenced from this repo 
-> https://github.com/atulapra/Emotion-detection/tree/master
"""

import cv2
import keras
import os

import numpy as np

from keras import layers

# recreate model from training.py script
model = keras.models.Sequential(
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

model.load_weights(os.path.join(os.getcwd(), 'model.h5'))

# one hot encode emotions
emotions: dict[int, str] = {
    0: "Angry", 1: "Disgusted", 2: "Fearful", 
    3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"
}

# load face detector model
classifier = cv2.CascadeClassifier(os.path.join(os.getcwd(), 'haarcascade_frontalface_default.xml'))

cap = cv2.VideoCapture(0)  # begin webcam feed
while True:
    ret, frame = cap.read()  # read success bool and frame
    if not ret:  # if ret is false, no frame was processed, so break loop
        break

    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert frame to greyscale
    faces = classifier.detectMultiScale(grey, scaleFactor=1.3, minNeighbors=5)  # detect faces
    # loop over face positions
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)  # draw a rectangle
        aoi = grey[y:y + h, x:x + w]  # get area of interest/specific face
        # crop the image for inputting in the facial expression model
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(aoi, (48, 48)), -1), 0)
        prediction = model.predict(cropped_img)  # predict emotions
        # get the index of the emotion with the highest probability of being correct
        idx = int(np.argmax(prediction))
        # draw the predicted emotion to the frame
        cv2.putText(
            frame, emotions[idx], (x+20, y-60), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # display the frame onto a window
    cv2.imshow('PsychTracker', cv2.resize(frame, (1600, 960), interpolation = cv2.INTER_CUBIC))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release camera and destroy all opencv windows
cap.release()
cv2.destroyAllWindows()