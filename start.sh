#!/bin/bash

mkdir -p /data/app/logs/dca-vc/
# mkdir -p /data/app/dca-vc/tmp
# mkdir -p ~/.keras/models
# cp models/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5 ~/.keras/models/

## auto run by aomp
# cd /data/app/dca-vc
# tar xvfz dca-vc-env.tar.gz

source bin/activate
nohup gunicorn --config gunicorn.conf vc:app >/dev/null &