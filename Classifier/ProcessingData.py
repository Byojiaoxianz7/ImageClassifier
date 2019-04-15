import os
import random
import shutil
import numpy as np
from PIL import Image
from Spider.Spider import Crawler


class ProcessingData(object):
    """
    定义一个处理数据的类
    功能：
    1, rename the images
    2, resize the images
    3, images type conversion
    4, create folder
    """

    def __init__(self, Raw_Images_Folder, Train_Folder, Test_Folder, Type):

        self.raw_images_folder = Raw_Images_Folder
        self.train_folder = Train_Folder
        self.test_folder = Test_Folder
        self.type = Type

        if not os.path.exists(self.raw_images_folder):
            os.mkdir(self.raw_images_folder)
        if not os.path.exists(self.train_folder):
            os.mkdir(self.train_folder)
        if not os.path.exists(self.test_folder):
            os.mkdir(self.test_folder)

    def renameImages(self, filePath, Type):
        """
        定义一个图像重命名的方法
        用于对图片的重命名
        方便提取标签
        :param filePath: 图片存在的一级目录
        :param Type:
        :return:
        """
        folder_counter = 0
        for eve_type_folder in Type:
            file_counter = 0
            folders = os.listdir(filePath + eve_type_folder)
            for eve_type_image in folders:
                file_counter += 1
                os.rename(src=filePath + eve_type_folder + '/' + eve_type_image,
                          dst=filePath + eve_type_folder + '/' + str(folder_counter) + '_' +
                              eve_type_image.split('.')[
                                  0] + '.jpg')
            folder_counter += 1

    def resizeImages(self, filePath, Type=None, dstPath=None, Width=100, Height=100):
        """
        定义一个调整图片尺寸大小的方法

        :param filePath:
        :param Type:
        :param dstPath:
        :param Width:
        :param Height:
        :return:
        """
        for eve_type_folder in Type:
            for eve_type_image in os.listdir(filePath + eve_type_folder):
                image_open = Image.open(fp=filePath + eve_type_folder + '/' + eve_type_image)
                try:
                    new_image = image_open.resize((Width, Height), Image.BILINEAR)
                    new_image.save(os.path.join(dstPath, os.path.basename(eve_type_image)))
                except Exception as e:
                    print(e)

    def readImages(self, fileName, folder):
        """
        定义一个将图片转换为numpy的array类型的方法
        :param fileName:
        :param folder:
        :return:  numpy array
        """
        images_open = Image.open(folder + fileName)
        return np.array(images_open)

    def moveImagesToTestFolder(self):
        pathDir = os.listdir(self.train_folder)  # 取图片的原始路径
        filenumber = len(pathDir)
        rate = 0.2  # 自定义抽取图片的比例，比方说100张抽20张，那就是0.2
        picknumber = int(filenumber * rate)  # 按照rate比例从文件夹中取一定数量图片
        sample = random.sample(pathDir, picknumber)  # 随机选取picknumber数量的样本图片
        for name in sample:
            shutil.move(self.train_folder + name, self.test_folder + name)
        return

    def initialize(self):

        crawler = Crawler(0.05)
        classes_num = int(input('Number of classes: '))
        for eve_keyword in range(classes_num):
            keyword = input('Keyword {}: '.format(eve_keyword + 1))
            page_num = int(input('Page Number: '))
            crawler.start(word=keyword, spider_page_num=page_num)


        self.renameImages(filePath=self.raw_images_folder, Type=self.type)
        self.resizeImages(filePath=self.raw_images_folder, Type=self.type, dstPath=self.train_folder)
        self.moveImagesToTestFolder()
