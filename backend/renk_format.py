import numpy as np

def to_grayscale(img):
    b = img[:,:,0].astype(np.float32)
    g = img[:,:,1].astype(np.float32)
    r = img[:,:,2].astype(np.float32)
    gray = b * 0.114 + g * 0.587 + r * 0.299
    return np.stack([gray, gray, gray], axis=2).astype(np.uint8)

def to_binary(img, threshold=127):
    gray = to_grayscale(img)[:,:,0]
    binary = np.zeros_like(gray)
    binary[gray >= threshold] = 255
    return np.stack([binary, binary, binary], axis=2).astype(np.uint8)

def colorspace_transform_hsv(img):
    # BGR to HSV
    img_f = img.astype(np.float32) / 255.0
    b, g, r = img_f[:,:,0], img_f[:,:,1], img_f[:,:,2]
    
    cmax = np.max(img_f, axis=2)
    cmin = np.min(img_f, axis=2)
    delta = cmax - cmin
    
    h = np.zeros_like(cmax)
    
    mask_r = (cmax == r) & (delta != 0)
    mask_g = (cmax == g) & (delta != 0)
    mask_b = (cmax == b) & (delta != 0)
    
    h[mask_r] = 60 * (((g[mask_r] - b[mask_r]) / delta[mask_r]) % 6)
    h[mask_g] = 60 * (((b[mask_g] - r[mask_g]) / delta[mask_g]) + 2)
    h[mask_b] = 60 * (((r[mask_b] - g[mask_b]) / delta[mask_b]) + 4)
    
    s = np.zeros_like(cmax)
    mask_cmax = cmax != 0
    s[mask_cmax] = delta[mask_cmax] / cmax[mask_cmax]
    
    v = cmax
    
    # Return as image for visualization (H: 0-179, S: 0-255, V: 0-255)
    hsv = np.stack([h / 2, s * 255, v * 255], axis=2).astype(np.uint8)
    return hsv

def colorspace_transform_ycbcr(img):
    img_f = img.astype(np.float32)
    b, g, r = img_f[:,:,0], img_f[:,:,1], img_f[:,:,2]
    
    y = 0.299 * r + 0.587 * g + 0.114 * b
    cb = -0.1687 * r - 0.3313 * g + 0.5 * b + 128
    cr = 0.5 * r - 0.4187 * g - 0.0813 * b + 128
    
    ycbcr = np.stack([y, cr, cb], axis=2) # OpenCV genelde YCrCb kullanır, görselleştirme için mantıklı bir sıralama
    return np.clip(ycbcr, 0, 255).astype(np.uint8)
