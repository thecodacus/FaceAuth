import tensorflow as tf
import copy
from tensorflow.python.platform import gfile
sess = tf.Session()
with sess.as_default():
	c = tf.constant(False, dtype=bool, shape=[], name='phase_train')
	for node in sess.graph.as_graph_def().node:
		if node.name == 'phase_train':
		    c_def = node


	model_filename ='savedModel/20180408-102900/20180408-102900.pb'
	OUTPUT_GRAPH_DEF_FILE='savedModel/20180408-102900/modified-20180408-102900.pb'

	with gfile.FastGFile(model_filename, 'rb') as f:
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(f.read())

		newGraph=tf.GraphDef()
		for node in graph_def.node:
			if node.name == 'phase_train':
				newGraph.node.extend([c_def])
			else:
				newGraph.node.extend([copy.deepcopy(node)])

	with tf.gfile.GFile(OUTPUT_GRAPH_DEF_FILE, "wb") as f:
		f.write(newGraph.SerializeToString())
	g_in = tf.import_graph_def(newGraph)


LOGDIR='logdir'
train_writer = tf.summary.FileWriter(LOGDIR)
train_writer.add_graph(sess.graph)