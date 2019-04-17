# coding:utf-8
import os
import uuid
import keras
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, render_template
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten
from keras.optimizers import SGD
from keras.layers import Conv2D, MaxPooling2D


# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'jpeg', 'JPEG'])
app = Flask(__name__)


def resize_image(image_name):
    img = Image.open('static/images/' + image_name)
    new_img = img.resize((100, 100), Image.BILINEAR)
    new_img.save(os.path.join('static/images/', os.path.basename(image_name)))


def read_image(filename):
    img = Image.open('static/images/' + filename).convert('RGB')
    return np.array(img)


def testcat(image_name):
    # 预处理图片 变成100 x 100
    resize_image(image_name)
    x_test = []

    x_test.append(read_image(image_name))

    x_test = np.array(x_test)

    x_test = x_test.astype('float32')
    x_test /= 255

    keras.backend.clear_session()  # 清理session  反复识别

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

    # load weights
    model.load_weights('weights.h5')
    classes = model.predict_classes(x_test)[0]

    # return result   0 1 2 3   标签
    return classes


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({
                "error": 1001,
                "msg": "Please check the type of image uploaded, only PNG, PNG, JPG, JPG, BMP, JPEG"
            })

        # 当前文件所在路径
        basepath = os.path.dirname(__file__)

        # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # 这里没有使用 secur_filename() 原因是上传文件的文件名如果存在@#$等字符，flask会自动屏蔽
        upload_path = os.path.join(basepath, 'static/images', f.filename)
        f.save(upload_path)

        # 对上传的文件进行重命名
        uuid_str = uuid.uuid4().hex
        new_filename = uuid_str + '.jpg'
        os.rename(src='static/images/' + f.filename, dst='static/images/' + new_filename)

        # 利用模型进行识别
        classes = testcat(image_name=new_filename)
        classes = str(classes)

        return render_template('upload_seccessful.html', classes=classes)
    return render_template('upload.html')


if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=8987, debug=True)
