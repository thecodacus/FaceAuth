import os
import re
import tensorflow as tf
from tensorflow.python.platform import gfile
from utils.exporter import TFModelExporter

def get_model_filenames(model_dir):
  files = os.listdir(model_dir)
  meta_files = [s for s in files if s.endswith('.meta')]
  if len(meta_files)==0:
      raise ValueError('No meta file found in the model directory (%s)' % model_dir)
  elif len(meta_files)>1:
      raise ValueError('There should not be more than one meta file in the model directory (%s)' % model_dir)
  meta_file = meta_files[0]
  ckpt = tf.train.get_checkpoint_state(model_dir)
  if ckpt and ckpt.model_checkpoint_path:
      ckpt_file = os.path.basename(ckpt.model_checkpoint_path)
      return meta_file, ckpt_file

  meta_files = [s for s in files if '.ckpt' in s]
  max_step = -1
  for f in files:
      step_str = re.match(r'(^model-[\w\- ]+.ckpt-(\d+))', f)
      if step_str is not None and len(step_str.groups())>=2:
          step = int(step_str.groups()[1])
          if step > max_step:
              max_step = step
              ckpt_file = step_str.groups()[0]
  return meta_file, ckpt_file


model_dir="./savedModel/20180408-102900"

exptr=TFModelExporter()
sess = tf.Session()
with sess.as_default():
    model_filename ='savedModel/20180408-102900/modified-20180408-102900.pb'

    with gfile.FastGFile(model_filename, 'rb') as f:
      graph_def = tf.GraphDef()
      graph_def.ParseFromString(f.read())


      g_in = tf.import_graph_def(graph_def)


    for op in sess.graph.get_operations():
      if ("embeddings" in op.name ):
        print(op.name)
    images_placeholder = sess.graph.get_tensor_by_name("import/input:0")
    embeddings = sess.graph.get_tensor_by_name("import/embeddings:0")
    #phase_train_placeholder = sess.graph.get_tensor_by_name("import/phase_train:0")

    #sess.run(tf.global_variables_initializer())
    #sess.run(tf.local_variables_initializer())
    
    # inputTensor=Input, phase=None outputTensor=Output, session=sess, modelName="model", version='1',exportPathBase='./models'
    exptr.export(inputTensor=images_placeholder, phase=None, outputTensor=embeddings, session=sess, modelName="model", version='2',exportPathBase='./models')
