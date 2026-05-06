import numpy as np

def rotate_image(img, angle=45):
    h, w, c = img.shape
    rads = np.deg2rad(angle)
    
    # Tuval boyutunu büyütmemek için orijinal boyutları kullanıyoruz
    new_w, new_h = w, h
    
    cx, cy = w // 2, h // 2
    ncx, ncy = new_w // 2, new_h // 2
    
    # Vectorized rotation
    X, Y = np.meshgrid(np.arange(new_w), np.arange(new_h))
    
    x = X - ncx
    y = Y - ncy
    
    old_x = (x * np.cos(-rads) - y * np.sin(-rads) + cx).astype(int)
    old_y = (x * np.sin(-rads) + y * np.cos(-rads) + cy).astype(int)
    
    valid_mask = (old_x >= 0) & (old_x < w) & (old_y >= 0) & (old_y < h)
    
    rotated_img = np.zeros((new_h, new_w, c), dtype=np.uint8)
    rotated_img[valid_mask] = img[old_y[valid_mask], old_x[valid_mask]]
    
    return rotated_img

def crop_image(img, start_x=10, start_y=10, width=200, height=200):
    h, w, _ = img.shape
    start_x = max(0, min(start_x, w-1))
    start_y = max(0, min(start_y, h-1))
    end_x = min(start_x + width, w)
    end_y = min(start_y + height, h)
    return img[start_y:end_y, start_x:end_x].copy()

def zoom_image(img, factor=2.0):
    if factor <= 0:
        return img
        
    h, w, c = img.shape
    new_h = int(h * factor)
    new_w = int(w * factor)
    
    # Vectorized nearest neighbor
    y_indices = (np.arange(new_h) / factor).astype(int)
    x_indices = (np.arange(new_w) / factor).astype(int)
    
    y_indices = np.clip(y_indices, 0, h - 1)
    x_indices = np.clip(x_indices, 0, w - 1)
    
    zoomed_img = img[y_indices[:, None], x_indices]
    
    # Ekranda (CSS) boyut değişmediği için yakınlaştırma efektini görebilmek adına
    # görüntünün merkezini orijinal boyuta kırpıyoruz.
    if factor > 1.0:
        start_y = (new_h - h) // 2
        start_x = (new_w - w) // 2
        return zoomed_img[start_y:start_y+h, start_x:start_x+w]
    else:
        # Uzaklaştırma yapılıyorsa orijinal boyutta siyah bir tuvale yerleştiriyoruz
        out = np.zeros_like(img)
        start_y = (h - new_h) // 2
        start_x = (w - new_w) // 2
        out[start_y:start_y+new_h, start_x:start_x+new_w] = zoomed_img
        return out
