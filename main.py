# coding:utf-8


import os
from Classifier.Training import Training
from Classifier.ProcessingData import ProcessingData




if __name__ == '__main__':
    raw_images_folder = '../Dataset/Raw_Images_Folder/'
    train_images_folder = '../Dataset/Train_Images_Folder/'
    test_images_folder = '../Dataset/Test_Images_Folder/'
    batch_size = 10
    epochs = 100

    # catType = ['孟买猫', '布偶猫', '暹罗猫', '英国短毛猫']
    # 读取 Dataset/Raw_images_folder 文件夹里的所有文件夹名  os.listdir()
    type = os.listdir(raw_images_folder)

    # initialize
    processing_data = ProcessingData(
        Raw_Images_Folder=raw_images_folder,
        Train_Folder=train_images_folder,
        Test_Folder=test_images_folder,
        Type=type,
    )

    training = Training(
        Train_Folder=train_images_folder,
        Test_Folder=test_images_folder,
        Batch_Size=batch_size,
        Epochs=epochs,
    )

    # processing data
    processing_data.initialize()

    # trianing
    training.train()
