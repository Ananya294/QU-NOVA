from tensorflow.keras.models import load_model as keras_load_model

def load_brats_model():
    return keras_load_model(r"E:\projects\QU_NOVA\backend\ml\brats_3d.hdf5", compile=False)
