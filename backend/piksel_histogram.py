import numpy as np

def histogram_stretch(img):
    out = np.zeros_like(img)
    for c in range(3):
        channel = img[:,:,c]
        cmin = np.min(channel)
        cmax = np.max(channel)
        
        if cmax > cmin:
            stretched = ((channel - cmin) / (cmax - cmin) * 255).astype(np.uint8)
            out[:,:,c] = stretched
        else:
            out[:,:,c] = channel
            
    return out

def reduce_contrast(img, factor=0.5):
    img_f = img.astype(np.float32)
    mean_val = 128.0
    reduced = mean_val + factor * (img_f - mean_val)
    reduced = np.clip(reduced, 0, 255).astype(np.uint8)
    return reduced
