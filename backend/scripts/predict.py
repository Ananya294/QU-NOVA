import numpy as np

def predict_segmentation(model, volume):
    vol = np.expand_dims(volume, axis=0)
    if vol.ndim == 4:
        vol = np.expand_dims(vol, axis=-1)
    soft_preds = model.predict(vol)
    mask = np.argmax(soft_preds, axis=-1)
    return mask[0]