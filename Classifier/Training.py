# coding:utf-8


import os
import sys
import numpy as np
from PIL import Image
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten
from keras.optimizers import SGD
from keras.layers import Conv2D, MaxPooling2D

o_path = os.getcwd()
sys.path.append(o_path)
from Classifier.ProcessingData import ProcessingData

class Training(object):

    def __init__(self, Train_Folder, Test_Folder, Batch_Size, Epochs):
        self.train_folder = Train_Folder
        self.test_folder = Test_Folder
        self.batch_size = Batch_Size
        self.epochs = Epochs

    def readImages(self, fileName, folder):
        """
        定义一个将图片转换为numpy的array类型的方法
        :param fileName:
        :param folder:
        :return:  numpy array
        """
        try:
            images_open = Image.open(folder + fileName)
            return np.array(images_open)
        except (OSError, NameError) as e:
            print(e)


    def train(self):
        train_img_list = []  # x_train
        train_label_list = []  # y_train

        test_img_list = []  # x_test
        test_lebal_list = []  # y_test

        # 将训练集图片转换成数组
        for file_1 in os.listdir(self.train_folder):
            file_img_to_array = self.readImages(fileName=file_1, folder=self.train_folder)
            train_img_list.append(file_img_to_array)
            train_label_list.append(int(file_1.split('_')[0]))

        train_img_list = np.array(train_img_list)
        train_label_list = np.array(train_label_list)

        # 将测试集图片转换成数组
        for file_2 in os.listdir(self.test_folder):
            file_img_to_array = self.readImages(fileName=file_2, folder=self.test_folder)
            test_img_list.append(file_img_to_array)
            test_lebal_list.append(int(file_2.split('_')[0]))

        test_img_list = np.array(test_img_list)
        test_lebal_list = np.array(test_lebal_list)

        # 将标签转化格式
        y_train = np_utils.to_categorical(y=train_label_list)
        y_test = np_utils.to_categorical(y=test_lebal_list)

        # 将特征点从0~255转换成0~1提高特征提取精度
        x_train = train_img_list.astype('float32')
        x_test = test_img_list.astype('float32')
        x_train /= 255
        x_test /= 255

        # 搭建卷积神经网络
        model = Sequential()
        model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3)))
        model.add(Conv2D(32, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(4, activation='softmax'))

        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        model.fit(
            x_train,
            y_train,
            batch_size=self.batch_size,  # 一轮训练10次
            epochs=self.epochs  # 一共训练32轮
        )
        model.save_weights('weights.h5', overwrite=True)
        score = model.evaluate(x_test, y_test, batch_size=10)

        x_train.shape()
        print(score)
