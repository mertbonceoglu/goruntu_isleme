import numpy as np

def manual_resize(img, target_w, target_h):
    """
    Nearest neighbor yöntemiyle görüntüyü yeniden boyutlandırır.
    İki farklı boyuttaki görüntüyü aritmetik işleme sokmadan önce
    boyutlarını eşitlemek için kullanıyoruz.
    """
    h, w, c = img.shape
    resized = np.zeros((target_h, target_w, c), dtype=np.uint8)
    
    for i in range(target_h):
        for j in range(target_w):
            # Orantılı eşleme: yeni koordinat * (eski boyut / yeni boyut)
            orig_i = int(i * h / target_h)
            orig_j = int(j * w / target_w)
            # Taşma kontrolü
            orig_i = min(orig_i, h-1)
            orig_j = min(orig_j, w-1)
            resized[i, j] = img[orig_i, orig_j]
    return resized

def subtract_images(img1, img2):
    """İki görüntü arasındaki farkı hesaplar. Negatif değerler 0'a kırpılır."""
    if img2 is None: return img1
    h, w, c = img1.shape
    # İkinci görüntüyü birincinin boyutuna getir
    img2_res = manual_resize(img2, w, h)
    
    # int16'ya çeviriyoruz çünkü uint8 ile çıkarma negatif veremez
    out = img1.astype(np.int16) - img2_res.astype(np.int16)
    out = np.clip(out, 0, 255).astype(np.uint8)
    return out

def multiply_images(img1, img2):
    """İki görüntünün piksellerini çarpar. 255'e bölerek normalize eder."""
    if img2 is None: return img1
    h, w, c = img1.shape
    img2_res = manual_resize(img2, w, h)
    
    # float32 ile çarpım yapıp 255'e bölüyoruz (0-255 aralığında kalması için)
    # Örn: 200 * 200 = 40000, bölü 255 ≈ 157
    out = (img1.astype(np.float32) * img2_res.astype(np.float32)) / 255.0
    out = np.clip(out, 0, 255).astype(np.uint8)
    return out
