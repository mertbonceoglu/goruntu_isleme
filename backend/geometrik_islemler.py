import numpy as np

def rotate_image(img, angle=45):
    """Görüntüyü merkez etrafında verilen açıda döndürür (ters dönüşüm yöntemiyle)."""
    h, w, c = img.shape
    rads = np.deg2rad(angle)
    
    # Çıktı boyutunu orijinalle aynı tutuyoruz (kenarlar kırpılır)
    new_w, new_h = w, h
    
    # Döndürme merkezi
    cx, cy = w // 2, h // 2
    ncx, ncy = new_w // 2, new_h // 2
    
    # meshgrid ile tüm piksel koordinatlarını oluştur
    X, Y = np.meshgrid(np.arange(new_w), np.arange(new_h))
    
    # Merkeze göre relatif koordinatlar
    x = X - ncx
    y = Y - ncy
    
    # Ters dönüşüm: hedef pikselin kaynak görüntüdeki karşılığını bul
    # (ileri dönüşümde boşluklar oluşabiliyor, bu yüzden tersten gidiyoruz)
    old_x = (x * np.cos(-rads) - y * np.sin(-rads) + cx).astype(int)
    old_y = (x * np.sin(-rads) + y * np.cos(-rads) + cy).astype(int)
    
    # Sınır dışı koordinatları filtrele
    valid_mask = (old_x >= 0) & (old_x < w) & (old_y >= 0) & (old_y < h)
    
    rotated_img = np.zeros((new_h, new_w, c), dtype=np.uint8)
    rotated_img[valid_mask] = img[old_y[valid_mask], old_x[valid_mask]]
    
    return rotated_img

def crop_image(img, start_x=10, start_y=10, width=200, height=200):
    """Görüntüden belirtilen bölgeyi keser. Sınır kontrolü yapar."""
    h, w, _ = img.shape
    # Başlangıç noktalarını görüntü sınırları içinde tut
    start_x = max(0, min(start_x, w-1))
    start_y = max(0, min(start_y, h-1))
    # Bitiş noktaları da sınırı aşmasın
    end_x = min(start_x + width, w)
    end_y = min(start_y + height, h)
    return img[start_y:end_y, start_x:end_x].copy()

def zoom_image(img, factor=2.0):
    """
    Nearest Neighbor interpolasyonla yakınlaştırma/uzaklaştırma.
    factor > 1: zoom in (merkez kırpılır)
    factor < 1: zoom out (siyah çerçeveye yerleşir)
    """
    if factor <= 0:
        return img
        
    h, w, c = img.shape
    new_h = int(h * factor)
    new_w = int(w * factor)
    
    # Orantılı eşleme: yeni koordinat / factor = eski koordinat
    y_indices = (np.arange(new_h) / factor).astype(int)
    x_indices = (np.arange(new_w) / factor).astype(int)
    
    # Taşma kontrolü
    y_indices = np.clip(y_indices, 0, h - 1)
    x_indices = np.clip(x_indices, 0, w - 1)
    
    # Fancy indexing ile tüm pikselleri aynı anda eşle
    zoomed_img = img[y_indices[:, None], x_indices]
    
    # Yakınlaştırma: büyütülmüş görüntünün merkezini orijinal boyuta kırp
    # (arayüzde panel boyutu sabit olduğu için bunu yapmak zorundayız)
    if factor > 1.0:
        start_y = (new_h - h) // 2
        start_x = (new_w - w) // 2
        return zoomed_img[start_y:start_y+h, start_x:start_x+w]
    else:
        # Uzaklaştırma: küçültülmüş görüntüyü siyah tuvale ortala
        out = np.zeros_like(img)
        start_y = (h - new_h) // 2
        start_x = (w - new_w) // 2
        out[start_y:start_y+new_h, start_x:start_x+new_w] = zoomed_img
        return out
