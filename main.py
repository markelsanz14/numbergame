import numpy as np
import csv
import tflearn
import tensorflow as tf
from sklearn.feature_selection import VarianceThreshold

def load_training_data(filename):
  data, labels = [], []
  with open(filename) as dataset_csv:
    reader = csv.reader(dataset_csv)
    next(reader, None) # skip header
    # extract feature vectors and labels
    for row in reader:
      labels.append(row.pop(-1))
      data.append(np.asarray(row, dtype=np.float32))
    data = np.array(data)
    sel = VarianceThreshold(threshold=.01)
    data = sel.fit_transform(data)
    labels = np.array(labels, dtype=np.int)
    labels = tflearn.data_utils.to_categorical(labels, 2)
    return (data, labels)

def load_input_data(filename):
  data, tags = [], []
  with open(filename) as dataset_csv:
    reader = csv.reader(dataset_csv)
    next(reader, None) # skip header
    # extract feature vectors and tags
    for row in reader:
      tags.append(row.pop(0))
      data.append(np.asarray(row, np.float))
    return (data, tags)

# process input data
t_data, t_labels = load_training_data('numerai_training_data.csv')

print(t_data)
print(t_labels)

# input layer takes an unspecified amount of 21-vectors
net = tflearn.input_data(shape=[None, 21])
net = tflearn.fully_connected(net, 32, bias_init='normal')
net = tflearn.fully_connected(net, 32, bias_init='normal')
net = tflearn.fully_connected(net, 2, activation='softmax')

sgd = tflearn.SGD(learning_rate=.7, lr_decay=0.96, decay_step=10000)
net = tflearn.regression(net, optimizer=sgd, loss='softmax_categorical_crossentropy')

model = tflearn.DNN(net)
model.fit(t_data, t_labels, n_epoch=500000, batch_size=256, show_metric=True)

with open("model.tf", 'w') as model_file:
  model.save(model_file)
  model_file.close()
