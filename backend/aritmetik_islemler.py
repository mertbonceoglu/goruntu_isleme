import numpy as np

def manual_resize(img, target_w, target_h):
    h, w, c = img.shape
    resized = np.zeros((target_h, target_w, c), dtype=np.uint8)
    
    for i in range(target_h):
        for j in range(target_w):
            orig_i = int(i * h / target_h)
            orig_j = int(j * w / target_w)
            # prevent out of bounds
            orig_i = min(orig_i, h-1)
            orig_j = min(orig_j, w-1)
            resized[i, j] = img[orig_i, orig_j]
    return resized

def add_images(img1, img2):
    if img2 is None: return img1
    h, w, c = img1.shape
    img2_res = manual_resize(img2, w, h)
    
    out = img1.astype(np.uint16) + img2_res.astype(np.uint16)
    out = np.clip(out, 0, 255).astype(np.uint8)
    return out

def subtract_images(img1, img2):
    if img2 is None: return img1
    h, w, c = img1.shape
    img2_res = manual_resize(img2, w, h)
    
    out = img1.astype(np.int16) - img2_res.astype(np.int16)
    out = np.clip(out, 0, 255).astype(np.uint8)
    return out

def multiply_images(img1, img2):
    if img2 is None: return img1
    h, w, c = img1.shape
    img2_res = manual_resize(img2, w, h)
    
    out = (img1.astype(np.float32) * img2_res.astype(np.float32)) / 255.0
    out = np.clip(out, 0, 255).astype(np.uint8)
    return out
