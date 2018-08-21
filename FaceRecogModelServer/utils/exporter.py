
import os
import tensorflow as tf

class TFModelExporter():
  def __init__(self):
    pass
  
  def export(self,
    inputTensor,  
    outputTensor,
    session,
    phase=None,  
    modelName="model", 
    version='1',
    exportPathBase='./models'):
    
    export_path_base = os.path.join(exportPathBase, modelName)
    export_path = os.path.join( tf.compat.as_bytes(export_path_base), tf.compat.as_bytes(str(version)))
    
    print('Exporting trained model to', export_path)
    
    builder = tf.saved_model.builder.SavedModelBuilder(export_path)

    tensor_info_input = tf.saved_model.utils.build_tensor_info(inputTensor)
    tensor_info_output = tf.saved_model.utils.build_tensor_info(outputTensor)

    inputSig={'input': tensor_info_input}
    outputSig={'output': tensor_info_output}
    if not (phase is None):
      tensor_info_phase = tf.saved_model.utils.build_tensor_info(phase)
      inputSig={'input': tensor_info_input,'phase':tensor_info_phase}


    signeture_def= tf.saved_model.signature_def_utils.build_signature_def( 
      inputs=inputSig, 
      outputs=outputSig,
      method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME)

    builder.add_meta_graph_and_variables( session, [tf.saved_model.tag_constants.SERVING],
        signature_def_map={
          'encode': (signeture_def)
        },
        main_op=tf.tables_initializer(),
        strip_default_attrs=True)

    builder.save()