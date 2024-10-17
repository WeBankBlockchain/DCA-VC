from keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.utils import load_img, img_to_array
import ssl
import numpy as np

ssl._create_default_https_context = ssl._create_unverified_context  # 下载模型的时候不想进行ssl证书校验

# !export TF_CPP_MIN_LOG_LEVEL=2  # 屏蔽警告信息 （这是在jupyter中执行的shell命令，可以去掉这行不影响结果）

# 初始化VGG16模型 include_top=False 是指不保留顶层的3个全连接网络层
model = VGG16(weights='imagenet', include_top=False)
# model.load_weights("./weights.h5", by_name=True, skip_mismatch=True)

def extract_feature(path):
    print('Extracting features from image %s' % path)
    """
    VGG16模型抽取图片特征
    """
    # 图片转成PIL的Image对象，并且对图片做了缩放
    img = load_img(path, target_size=(224, 224))

    # 图片转成矩阵、并扩充了维度、最后是预处理
    predict_img = preprocess_input(np.expand_dims(img_to_array(img), 0))

    # 丢入vgg16网络做特征抽取，最后返回特征并展平成一维向量方便计算余弦相似度
    return model.predict(predict_img).flatten()
