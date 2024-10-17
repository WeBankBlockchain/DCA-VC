import os
import time
from flask import Flask, request, jsonify, make_response
from configparser import ConfigParser
from Log import Log
import vgg_extractor
import json
import threading


config_file = 'config.conf'
UPLOAD_FOLDER = 'upload'
log = Log().get_logger()
local_path = threading.local()

class ConfigInfo:
    def __init__(self, filename):
        cf = ConfigParser()
        cf.read(filename)
        log.info("read config start")
        self.port = cf.get("system", "port")
        self.tmpDir = cf.get("system", "tmpDir")
        log.info("read config end")


config = ConfigInfo(config_file)
basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.tmpDir  # 设置文件上传的目标文件夹


@app.route('/compute/feature', methods=['POST'])
def api_compute_feature():
    times = time.time()
    local_path.times = times
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])  # 拼接成合法文件夹地址
    seqNo = request.form.get('seqNo')
    local_path.seqNo = seqNo
    log.info("transaction {} started" , seqNo)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    f = request.files['file']
    # 存储到本地
    tmpFile = f'{time.time_ns()}{os.getpid()}'
    path = os.path.join(file_dir, tmpFile)
    local_path.path=path
    f.stream.seek(0)
    f.save(path)  # 保存文件到upload目录
    log.info("file save in {}" , path)
    features = vgg_extractor.extract_feature(path)
    vector = json.dumps(features.tolist())
    res = jsonify({
        "responseCode": "0",
        "responseMessage": "Success",
        "vector": vector,
    })
    rst = make_response(res)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    os.remove(path)
    used = str((time.time() - times)*1000)
    log.info("{} succeed", seqNo)
    monitorLogs = f'{{"code": "computeFeature","bizSeqNo": {seqNo},"resCode": "000000000","message": "Success","usedTime": {used}}}'
    log.bind(app=True).info(monitorLogs)
    log.debug("vector: " + vector)
    return rst, 200


@app.errorhandler(Exception)
def framework_error(e):
    os.remove(local_path.path)
    log.error("OnError: %s" % e)
    log.exception(e)
    res = jsonify({
        "responseCode": "1782T00010500",
        "responseMessage": "INTERNAL_ERROR"
    })
    seqNo = local_path.seqNo
    used = str((time.time() - local_path.times)*1000)
    monitorLogs = f'{{"code": "computeFeature","bizSeqNo": {seqNo},"resCode": "1782T00010500","message": "failed","usedTime": {used}}}'
    log.bind(app=True).info(monitorLogs)
    rst = make_response(res)
    return rst, 500


if __name__ == '__main__':
    app.run(port=int(config.port))
    log.info("test")
