document.addEventListener('DOMContentLoaded', () => {
    const menuBtns = document.querySelectorAll('.menu-btn');
    const currentActionTitle = document.getElementById('current-action-title');
    const panel2 = document.getElementById('panel2');
    
    // Dosya yükleme ve önizleme
    const file1 = document.getElementById('file1');
    const preview1 = document.getElementById('preview1');
    const placeholder1 = document.getElementById('placeholder1');
    const upload1 = document.getElementById('upload1');

    const file2 = document.getElementById('file2');
    const preview2 = document.getElementById('preview2');
    const placeholder2 = document.getElementById('placeholder2');
    const upload2 = document.getElementById('upload2');

    const processBtn = document.getElementById('process-btn');
    const undoBtn = document.getElementById('undo-btn');
    const resultImg = document.getElementById('result-img');
    const resultPlaceholder = document.getElementById('result-placeholder');
    const loader = document.getElementById('loader');
    const resetBtn = document.getElementById('reset-btn');
    const downloadBtn = document.getElementById('download-btn');

    // Sliders
    const slidersContainer = document.getElementById('sliders-container');

    // Histogram Modal
    const histogramModal = document.getElementById('histogram-modal');
    const closeBtn = document.querySelector('.close-btn');
    const histogramImg = document.getElementById('histogram-img');
    const histogramLoader = document.getElementById('histogram-loader');

    let historyStack = [];
    let currentOperation = 'gray';
    const currentActionDesc = document.getElementById('current-action-desc');

    // İşlem Açıklamaları
    const operationDescriptions = {
        'gray': 'Görüntüyü gri tonlamaya dönüştürür.',
        'binary': 'Pikselleri eşik değerine göre siyah veya beyaza çevirir.',
        'colorspace_hsv': 'Renk uzayını RGB\'den HSV formatına dönüştürür.',
        'colorspace_ycbcr': 'Renk uzayını RGB\'den YCbCr formatına dönüştürür.',
        'rotate': 'Görüntüyü belirlenen açıda döndürür.',
        'crop': 'Görüntünün seçilen bölgesini keser.',
        'zoom': 'Görüntüyü yakınlaştırır veya uzaklaştırır.',
        'show_histogram': 'Görüntünün piksel yoğunluk dağılımını gösterir.',
        'hist_stretch': 'Histogramı gererek kontrastı artırır.',
        'contrast': 'Görüntünün kontrastını belirlenen oranda azaltır.',
        'noise_sp': 'Görüntüye rastgele tuz-biber gürültüsü ekler.',
        'filter_mean': 'Ortalama filtresi ile görüntüyü yumuşatır.',
        'filter_median': 'Medyan filtresi ile gürültüyü temizler.',
        'filter_motion': 'Hareket bulanıklığı efekti uygular.',
        'threshold_double': 'Pikselleri iki eşik değerine göre sınıflandırır.',
        'canny': 'Görüntüdeki kenarları tespit eder.',
        'dilate': 'Parlak bölgeleri genişleterek nesneleri büyütür.',
        'erode': 'Parlak bölgeleri aşındırarak nesneleri küçültür.',
        'open': 'Önce aşındırıp sonra genişleterek gürültüyü temizler.',
        'close': 'Önce genişletip sonra aşındırarak boşlukları doldurur.',
        'arithmetic_sub': 'Bir görüntünün piksellerini diğerinden çıkararak fark görüntüsü oluşturur.',
        'arithmetic_mul': 'İki görüntünün piksel değerlerini çarpar.'
    };

    // Bildirim sistemi
    function showToast(message, type = 'error') {
        const container = document.getElementById('toast-container');
        if (!container) return;
        
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const iconSvg = type === 'error' 
            ? '<svg viewBox="0 0 24 24" width="20" height="20" stroke="#ef4444" stroke-width="2" fill="none"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>'
            : '<svg viewBox="0 0 24 24" width="20" height="20" stroke="#3b82f6" stroke-width="2" fill="none"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>';
            
        toast.innerHTML = `${iconSvg} <span>${message}</span>`;
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('toast-hide');
            setTimeout(() => toast.remove(), 400);
        }, 3000);
    }

    // Slider ayarları
    const operationSliders = {
        'binary': [
            { id: 'param1', label: 'Eşik Değeri', min: 0, max: 255, step: 1, value: 127 }
        ],
        'rotate': [
            { id: 'param1', label: 'Döndürme Açısı (Derece)', min: -180, max: 180, step: 1, value: 45 }
        ],
        'zoom': [
            { id: 'param1', label: 'Yakınlaştırma Oranı (%)', min: 10, max: 500, step: 10, value: 200 }
        ],
        'crop': [
            { id: 'param1', label: 'Başlangıç X', min: 0, max: 2000, step: 10, value: 50 },
            { id: 'param2', label: 'Başlangıç Y', min: 0, max: 2000, step: 10, value: 50 },
            { id: 'param3', label: 'Genişlik', min: 50, max: 2000, step: 1, value: 300 },
            { id: 'param4', label: 'Yükseklik', min: 50, max: 2000, step: 1, value: 300 }
        ],
        'contrast': [
            { id: 'param1', label: 'Kontrast Azaltma Miktarı (%)', min: 0, max: 100, step: 5, value: 50 }
        ],
        'noise_sp': [
            { id: 'param1', label: 'Gürültü Yoğunluğu (%)', min: 1, max: 20, step: 1, value: 5 }
        ],
        'filter_mean': [
            { id: 'param1', label: 'Filtre Boyutu', min: 3, max: 15, step: 2, value: 3 }
        ],
        'filter_median': [
            { id: 'param1', label: 'Filtre Boyutu', min: 3, max: 15, step: 2, value: 3 }
        ],
        'filter_motion': [
            { id: 'param1', label: 'Filtre Boyutu', min: 3, max: 31, step: 2, value: 9 }
        ],
        'threshold_double': [
            { id: 'param1', label: 'Alt Eşik', min: 0, max: 255, step: 1, value: 50 },
            { id: 'param2', label: 'Üst Eşik', min: 0, max: 255, step: 1, value: 150 }
        ],
        'dilate': [
            { id: 'param1', label: 'Çekirdek Boyutu', min: 3, max: 15, step: 2, value: 3 }
        ],
        'erode': [
            { id: 'param1', label: 'Çekirdek Boyutu', min: 3, max: 15, step: 2, value: 3 }
        ],
        'open': [
            { id: 'param1', label: 'Çekirdek Boyutu', min: 3, max: 15, step: 2, value: 3 }
        ],
        'close': [
            { id: 'param1', label: 'Çekirdek Boyutu', min: 3, max: 15, step: 2, value: 3 }
        ]
    };

    function renderSliders(operation) {
        slidersContainer.innerHTML = '';
        const sliders = operationSliders[operation];
        if (!sliders) return;

        sliders.forEach(slider => {
            const group = document.createElement('div');
            group.className = 'slider-group';
            
            const label = document.createElement('label');
            label.textContent = slider.label;
            label.style.display = 'block';
            label.style.marginBottom = '6px';
            
            const controlsDiv = document.createElement('div');
            controlsDiv.style.display = 'flex';
            controlsDiv.style.gap = '12px';
            controlsDiv.style.alignItems = 'center';
            
            const input = document.createElement('input');
            input.type = 'range';
            input.id = `range-${slider.id}`;
            input.min = slider.min;
            input.max = slider.max;
            input.step = slider.step;
            input.value = slider.value;
            input.style.flex = '1';

            const numberInput = document.createElement('input');
            numberInput.type = 'number';
            numberInput.id = slider.id; // Backend'in okuması için id'si bu olacak
            numberInput.min = slider.min;
            numberInput.max = slider.max;
            numberInput.step = slider.step;
            numberInput.value = slider.value;
            numberInput.className = 'number-input';
            numberInput.style.width = '70px';
            numberInput.style.padding = '6px';
            numberInput.style.borderRadius = '4px';
            numberInput.style.border = '1px solid rgba(255,255,255,0.2)';
            numberInput.style.backgroundColor = 'rgba(0,0,0,0.2)';
            numberInput.style.color = '#fff';
            numberInput.style.textAlign = 'center';

            input.addEventListener('input', (e) => {
                numberInput.value = e.target.value;
            });
            numberInput.addEventListener('input', (e) => {
                input.value = e.target.value;
            });

            controlsDiv.appendChild(input);
            controlsDiv.appendChild(numberInput);

            group.appendChild(label);
            group.appendChild(controlsDiv);
            slidersContainer.appendChild(group);
        });
    }

    // Açılır menü mantığı
    const accordionHeaders = document.querySelectorAll('.accordion-header');
    accordionHeaders.forEach(header => {
        header.addEventListener('click', () => {
            header.classList.toggle('active');
            const submenu = header.nextElementSibling;
            submenu.classList.toggle('open');
        });
    });

    // Menü mantığı
    menuBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            menuBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            currentActionTitle.textContent = btn.textContent;
            currentOperation = btn.dataset.action;
            currentActionDesc.textContent = operationDescriptions[currentOperation] || '';

            renderSliders(currentOperation);

            if (currentOperation.startsWith('arithmetic')) {
                panel2.style.display = 'flex';
            } else {
                panel2.style.display = 'none';
            }
        });
    });

    // İlk yükleme
    renderSliders(currentOperation);

    // Yükleme işlemi
    upload1.addEventListener('click', () => file1.click());
    upload2.addEventListener('click', () => file2.click());

    file1.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview1.src = e.target.result;
                preview1.style.display = 'block';
                placeholder1.style.display = 'none';
                
                // Sonuç alanında orijinal görüntüyü göster
                resultImg.src = e.target.result;
                resultImg.style.display = 'block';
                resultPlaceholder.style.display = 'none';
                
                historyStack = [e.target.result];
                updateUndoButton();
                
                preview1.onload = function() {
                    if(operationSliders['crop']) {
                        operationSliders['crop'][0].max = preview1.naturalWidth;
                        operationSliders['crop'][1].max = preview1.naturalHeight;
                        operationSliders['crop'][2].max = preview1.naturalWidth;
                        operationSliders['crop'][3].max = preview1.naturalHeight;
                        if (currentOperation === 'crop') renderSliders('crop');
                    }
                };
            }
            reader.readAsDataURL(file);
        }
    });

    file2.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview2.src = e.target.result;
                preview2.style.display = 'block';
                placeholder2.style.display = 'none';
            }
            reader.readAsDataURL(file);
        }
    });

    function updateUndoButton() {
        undoBtn.disabled = historyStack.length <= 1;
        resetBtn.disabled = historyStack.length <= 1;
        downloadBtn.disabled = historyStack.length <= 1;
    }

    undoBtn.addEventListener('click', () => {
        if (historyStack.length > 1) {
            historyStack.pop();
            resultImg.src = historyStack[historyStack.length - 1];
            updateUndoButton();
        }
    });

    resetBtn.addEventListener('click', () => {
        if (historyStack.length > 1) {
            const baseImg = historyStack[0];
            historyStack = [baseImg];
            resultImg.src = baseImg;
            updateUndoButton();
        }
    });

    downloadBtn.addEventListener('click', () => {
        if (historyStack.length > 1) {
            const link = document.createElement('a');
            link.href = historyStack[historyStack.length - 1];
            link.download = 'islenmis_goruntu.png';
            link.click();
        }
    });

    // Klavye kısayolları
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && (e.key === 'z' || e.key === 'Z')) {
            e.preventDefault();
            if (!undoBtn.disabled) {
                undoBtn.click();
            }
        }
    });

    closeBtn.onclick = function() {
        histogramModal.style.display = "none";
    }
    window.onclick = function(event) {
        if (event.target == histogramModal) {
            histogramModal.style.display = "none";
        }
    }

    async function getFileToProcess() {
        if (historyStack.length > 0) {
            const res = await fetch(historyStack[historyStack.length - 1]);
            const blob = await res.blob();
            return new File([blob], "image.png", { type: "image/png" });
        } else {
            return file1.files[0];
        }
    }

    processBtn.addEventListener('click', async () => {
        if (!file1.files[0] && historyStack.length === 0) {
            showToast('Lütfen önce birinci görüntüyü yükleyin!');
            return;
        }

        const currentFile = await getFileToProcess();

        if (currentOperation === 'show_histogram') {
            histogramModal.style.display = 'block';
            histogramImg.style.display = 'none';
            histogramLoader.style.display = 'block';

            const formData = new FormData();
            formData.append('file', currentFile);

            try {
                const response = await fetch('/histogram', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                if (response.ok) {
                    histogramImg.src = data.histogram_image;
                    histogramImg.style.display = 'block';
                } else {
                    showToast('Hata: ' + data.message);
                }
            } catch (error) {
                showToast('Sunucuya bağlanılamadı.');
            } finally {
                histogramLoader.style.display = 'none';
            }
            return;
        }

        if (currentOperation.startsWith('arithmetic') && !file2.files[0]) {
            showToast('Bu işlem için ikinci görüntüyü yüklemeniz gereklidir!');
            return;
        }

        const formData = new FormData();
        formData.append('file1', currentFile);
        if (file2.files[0]) {
            formData.append('file2', file2.files[0]);
        }
        formData.append('operation', currentOperation);
        
        // Slider parametrelerini ekle
        const currentSliders = operationSliders[currentOperation];
        if (currentSliders) {
            currentSliders.forEach(slider => {
                const el = document.getElementById(slider.id);
                if (el) formData.append(slider.id, el.value);
            });
        }

        resultImg.style.display = 'none';
        resultPlaceholder.style.display = 'none';
        loader.style.display = 'inline-block';
        processBtn.disabled = true;

        try {
            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                resultImg.src = data.processed_image;
                resultImg.style.display = 'block';
                historyStack.push(data.processed_image);
                updateUndoButton();
            } else {
                showToast('Hata: ' + data.message);
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('Sunucuya bağlanılamadı.');
        } finally {
            loader.style.display = 'none';
            processBtn.disabled = false;
        }
    });
});
