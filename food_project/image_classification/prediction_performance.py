#!/usr/bin/env python

'''Implement function to check prediction performance per class'''

import tensorflow as tf
import numpy as np
import pandas as pd
import pickle

partition = 'validation'
path = partition + '_ds'
spec = (tf.TensorSpec(shape=(None, 256, 256, 3), dtype=tf.float32, name=None), tf.TensorSpec(shape=(None,), dtype=tf.int32, name=None))

val_data = tf.data.experimental.load(path, spec)
trained_model = tf.keras.models.load_model('hyvee.best.hdf5')

# val_data_x = val_data.map(lambda x, y: x)
# val_data_y = val_data.map(lambda x, y: y)
# preds = trained_model.predict(val_data_x)


preds = []
y_trues = []
i = 0
for val_batch in val_data:
    logits = trained_model.predict(val_batch[0])
    y_trues.append(val_batch[1])
    preds.append(tf.argmax(tf.nn.softmax(logits), axis=1))
    i += 1
    if i == len(val_data):
        break

preds_ = tf.reshape(tf.stack(preds[:-1]), -1).numpy()
y_trues_ = tf.reshape(tf.stack(y_trues[:-1]), -1).numpy()

preds = tf.concat([preds_, preds[-1]], axis=0)
y_trues = tf.concat([y_trues_, y_trues[-1]], axis=0)


# row True, column predicted
conf_matrix = np.zeros((130, 130))

for cls in range(130):
    inds = y_trues == cls

    for cls_pred in range(130):
        conf_matrix[cls, cls_pred] = sum((preds[inds]==cls_pred).numpy())


with open('hyvee_label.dict', 'rb') as f:
    mapping = pickle.load(f)

reverse_map = {v:k for k,v in mapping.items()}
ings = [x[1] for x in sorted(reverse_map.items(), key=lambda x: x[0])]
conf_matrix = pd.DataFrame(conf_matrix)
conf_matrix.columns = ings
conf_matrix.index = ings
conf_matrix.to_csv(f"inceptionv3_{partition}_confusion_matrix.csv")
