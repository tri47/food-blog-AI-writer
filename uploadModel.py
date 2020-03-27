import os
import boto3
import sys
import threading
import sys
import os
import time
import json
import numpy as np
import re
import tensorflow as tf
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def

sys.path.append(os.path.join(os.getcwd(), 'gpt-2/src'))
import model, sample

def export_for_serving(
    model_name='124M',
    seed=None,
    batch_size=1,
    length=None,
    temperature=1,
    top_k=0,
    models_dir='models'
):
    models_dir = 'models'# os.path.expanduser(os.path.expandvars(models_dir))

    hparams = model.default_hparams()
    with open(os.path.join(models_dir, model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))

    if length is None:
        length = hparams.n_ctx
    elif length > hparams.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

    with tf.Session(graph=tf.Graph()) as sess:
        context = tf.placeholder(tf.int32, [batch_size, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)

        output = sample.sample_sequence(
            hparams=hparams, length=length,
            context=context,
            batch_size=batch_size,
            temperature=temperature, top_k=top_k
        )

        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(models_dir, model_name))
        saver.restore(sess, ckpt)

        export_dir=os.path.join(models_dir, model_name, "export", str(time.time()).split('.')[0])
        if not os.path.isdir(export_dir):
            os.makedirs(export_dir)

        builder = tf.saved_model.builder.SavedModelBuilder(export_dir)
        signature = predict_signature_def(inputs={'context': context},
        outputs={'sample': output})

        builder.add_meta_graph_and_variables(sess,
                                     [tf.saved_model.SERVING],
                                     signature_def_map={"predict": signature},
                                     strip_default_attrs=True)
        builder.save()


export_for_serving(top_k=40, length=256, model_name='captionModel')


directory = '/models/captionModel/'
directory = '/'

bucket = 'gpt-2-models'

class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(directory+ filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()

s3 = boto3.client("s3")

for filename in os.listdir(directory):
    print(filename)
    s3.upload_file(directory + filename, bucket , "captionModel/" + filename,
    Callback=ProgressPercentage(filename))

'
#print("\nUploaded model export directory to {}/{}".format(S3_UPLOAD_PATH, MODEL_SIZE))
for dirpath, _, filenames in os.walk("models/{}/export".format('captionModel')):
    for filename in filenames: #os.listdir(directory):
        print(dirpath)
        print(filename)
        if filename != '.DS_Store':
           s3.upload_file(dirpath + '/' + filename, bucket , "captionModel/new/" + dirpath )#,
#Callback=ProgressPercentage(dirpath+'/'+filename))