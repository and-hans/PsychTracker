"""
Model and code was referenced from this repo 
-> https://github.com/atulapra/Emotion-detection/tree/master
"""
import keras
import os

from keras import layers
from keras.preprocessing.image import ImageDataGenerator

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # get rid of tensorflow logs 

# training and validation testing data directory paths
train_pth: str = os.path.join(os.getcwd(), 'data/train')
validation_pth: str = os.path.join(os.getcwd(), 'data/test')

# create an image data generator and normalize the values
train_datagen = ImageDataGenerator(rescale = 1./255)  
validation_datagen = ImageDataGenerator(rescale = 1./255)

batch_size: int = 64

# get the training and validation data
train_generator = train_datagen.flow_from_directory(
        train_pth,
        batch_size = batch_size,
        class_mode = 'categorical',
        color_mode = "grayscale",
        target_size = (48, 48))

validation_generator = validation_datagen.flow_from_directory(
        validation_pth,
        batch_size = batch_size,
        class_mode = 'categorical',
        color_mode = "grayscale",
        target_size = (48, 48))

# create model a 3 layer model 
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

# set models loss function, optimizer, and metric 
model.compile(
    loss = 'categorical_crossentropy',
    optimizer = keras.optimizers.Adam(learning_rate=0.0001, decay=1e-6),
    metrics = ['accuracy'])

num_train: int = 28709  # number of images in the training set
num_val: int = 7178  # number of images in the validation set
num_epoch: int = 50  

# train model
model_info = model.fit(
        train_generator,
        steps_per_epoch = num_train // batch_size,
        epochs = num_epoch,
        validation_data = validation_generator,
        validation_steps = num_val // batch_size)

model.save_weights(os.path.join(os.getcwd(), 'model.h5'))  # save model weights