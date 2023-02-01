# Model uses CNN to predict the price of an artwork based on the image
import pandas as pd
import numpy as np
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
import joblib

# Load the csv file into a pandas dataframe
df = pd.read_csv("artDataset.csv")
df["price"] = df["price"].astype('int32')

# Split the dataframe into train and test sets
train_df, test_df = train_test_split(df, test_size=0.2)

# Define the image data generator
img_width, img_height = 150, 150
batch_size = 32

data_gen = ImageDataGenerator(rescale=1./255)

# Create the train and test generators
train_generator = data_gen.flow_from_dataframe(
    dataframe=train_df,
    directory='/home/cdsw/ArtData/artDataset',
    x_col='Title',
    y_col='price',
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='other')

test_generator = data_gen.flow_from_dataframe(
    dataframe=test_df,
    directory='/home/cdsw/ArtData/artDataset',
    x_col='Title',
    y_col='price',
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='other')

# Define the model
model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape=(img_width, img_height, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))

model.compile(loss='mean_squared_error', optimizer='adam')

# Define the callbacks
checkpointer = ModelCheckpoint(filepath='model.weights.best.hdf5', verbose=1, save_best_only=True)
model.fit(train_generator,
          steps_per_epoch=train_generator.samples // batch_size,
          validation_data=test_generator,
          validation_steps=test_generator.samples // batch_size,
          epochs=30,
          callbacks=[checkpointer])
test_mae = model.evaluate(x=test_generator, verbose=0)
print('Test MAE:', test_mae)

joblib.dump(model, 'image_regressor.joblib')
