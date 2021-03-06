import os
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense, Activation
from keras.layers.convolutional import Convolution2D, MaxPooling2D
import time

start = time.time()

train_data_path = 'data/train'
validation_data_path = 'data/validation'


#Parameters
img_width, img_height = 150, 150
batch_size = 32
epochs = 50
validation_steps = 300
nb_filters1 = 32
nb_filters2 = 64
conv1_size = 3
conv2_size = 2
pool_size = 2
classes_num = 3
lr = 0.0004

"""
Feature Extraction
"""
model = Sequential()
model.add(Convolution2D(nb_filters1, conv1_size, input_shape=(img_width, img_height, 3)))
model.add(Activation("relu")) #Rectifier Linear Unit
model.add(MaxPooling2D(pool_size=(pool_size, pool_size)))

model.add(Convolution2D(nb_filters2, conv2_size, conv2_size))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(pool_size, pool_size)))

"""
Fully Connected
"""
model.add(Flatten())
model.add(Dense(256))
model.add(Activation("relu"))
model.add(Dropout(0.5))
model.add(Dense(classes_num, activation='softmax'))

"""
Compile Architecture CNN
"""
model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.RMSprop(lr=lr),
              metrics=['acc'])

"""
Setting Preparation dataset
"""
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_path,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
    validation_data_path,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')

"""
Training
"""
model.fit_generator(
    train_generator,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=validation_steps)

target_dir = './models/'
if not os.path.exists(target_dir):
    os.mkdir(target_dir)
model.save('./models/model.h5')

# Calculate execution time
end = time.time()
dur = end - start

if dur < 60:
    print("Execution Time:", dur, "seconds")
elif 60 < dur < 3600:
    dur = dur / 60
    print("Execution Time:", dur, "minutes")
else:
    dur = dur / (60 * 60)
    print("Execution Time:", dur, "hours")
