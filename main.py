# -*- coding:utf-8 -*-

import os
import sys

o_path = os.getcwd()
sys.path.append(o_path)

from Classifier.ProcessingData import ProcessingData
from Classifier.Training import Training
from Spider.Spider import Crawler


def main():
    raw_images_folder = './Dataset/Raw_Images_Folder/'
    train_images_folder = './Dataset/Train_Images_Folder/'
    test_images_folder = './Dataset/Test_Images_Folder/'
    batch_size = 10
    epochs = 100


    crawler = Crawler(0.05)
    # classes_num = int(input('Number of classes: '))

    # for eve_keyword in range(classes_num):
    # keyword = input('Keyword {}: '.format(eve_keyword + 1))
    # page_num = int(input('Page Number: '))

    # crawler.start("孟买猫", 1, 1)
    # crawler.start("布偶猫", 1, 1)
    # crawler.start("暹罗猫", 1, 1)
    # crawler.start("英国短毛猫", 1, 1)


    # catType = ['孟买猫', '布偶猫', '暹罗猫', '英国短毛猫']
    # 读取 Dataset/Raw_images_folder 文件夹里的所有文件夹名  os.listdir()

    type = os.listdir(raw_images_folder)
    print(type)

    # initialize
    processing_data = ProcessingData(
        Raw_Images_Folder=raw_images_folder,
        Train_Folder=train_images_folder,
        Test_Folder=test_images_folder,
        Type=type,
    )

    # processing data
    processing_data.initialize()


    training = Training(
        Train_Folder=train_images_folder,
        Test_Folder=test_images_folder,
        Batch_Size=batch_size,
        Epochs=epochs,
    )

    # trianing
    training.train()


if __name__ == '__main__':
    main()
