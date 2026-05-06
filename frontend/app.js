document.addEventListener('DOMContentLoaded', () => {
    const menuBtns = document.querySelectorAll('.menu-btn');
    const currentActionTitle = document.getElementById('current-action-title');
    const panel2 = document.getElementById('panel2');
    
    // File inputs & previews
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

    // Sliders
    const slidersContainer = document.getElementById('sliders-container');

    // Histogram Modal
    const histogramModal = document.getElementById('histogram-modal');
    const closeBtn = document.querySelector('.close-btn');
    const histogramImg = document.getElementById('histogram-img');
    const histogramLoader = document.getElementById('histogram-loader');

    let historyStack = [];
    let currentOperation = 'gray';

    // Slider Configurations
    const operationSliders = {
        'rotate': [
            { id: 'param1', label: 'Döndürme Açısı (Derece)', min: -180, max: 180, step: 1, value: 45 }
        ],
        'zoom': [
            { id: 'param1', label: 'Yakınlaştırma Oranı (%)', min: 10, max: 500, step: 10, value: 200 }
        ],
        'crop': [
            { id: 'param1', label: 'Başlangıç X', min: 0, max: 2000, step: 10, value: 50 },
            { id: 'param2', label: 'Başlangıç Y', min: 0, max: 2000, step: 10, value: 50 },
            { id: 'param3', label: 'Genişlik', min: 50, max: 2000, step: 10, value: 300 },
            { id: 'param4', label: 'Yükseklik', min: 50, max: 2000, step: 10, value: 300 }
        ],
        'noise_sp': [
            { id: 'param1', label: 'Gürültü Yoğunluğu (%)', min: 1, max: 20, step: 1, value: 5 }
        ],
        'filter_mean': [
            { id: 'param1', label: 'Bulanıklık Derecesi (Bölge Boyutu)', min: 3, max: 15, step: 2, value: 3 }
        ],
        'filter_median': [
            { id: 'param1', label: 'Bulanıklık Derecesi (Bölge Boyutu)', min: 3, max: 15, step: 2, value: 3 }
        ],
        'filter_motion': [
            { id: 'param1', label: 'Bulanıklık Şiddeti (Kernel)', min: 3, max: 31, step: 2, value: 9 }
        ],
        'threshold_double': [
            { id: 'param1', label: 'Alt Eşik', min: 0, max: 255, step: 1, value: 50 },
            { id: 'param2', label: 'Üst Eşik', min: 0, max: 255, step: 1, value: 150 }
        ],
        'dilate': [
            { id: 'param1', label: 'Etki Miktarı (Bölge Boyutu)', min: 3, max: 15, step: 2, value: 3 }
        ],
        'erode': [
            { id: 'param1', label: 'Etki Miktarı (Bölge Boyutu)', min: 3, max: 15, step: 2, value: 3 }
        ],
        'open': [
            { id: 'param1', label: 'Etki Miktarı (Bölge Boyutu)', min: 3, max: 15, step: 2, value: 3 }
        ],
        'close': [
            { id: 'param1', label: 'Etki Miktarı (Bölge Boyutu)', min: 3, max: 15, step: 2, value: 3 }
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

    // Accordion Logic
    const accordionHeaders = document.querySelectorAll('.accordion-header');
    accordionHeaders.forEach(header => {
        header.addEventListener('click', () => {
            header.classList.toggle('active');
            const submenu = header.nextElementSibling;
            submenu.classList.toggle('open');
        });
    });

    // Menu logic
    menuBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            menuBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            currentActionTitle.textContent = btn.textContent;
            currentOperation = btn.dataset.action;

            renderSliders(currentOperation);

            if (currentOperation.startsWith('arithmetic')) {
                panel2.style.display = 'flex';
            } else {
                panel2.style.display = 'none';
            }
        });
    });

    // Initial render
    renderSliders(currentOperation);

    // Upload logic
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
                historyStack = [];
                updateUndoButton();
                resultImg.style.display = 'none';
                resultPlaceholder.style.display = 'flex';
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
        undoBtn.disabled = historyStack.length === 0;
    }

    undoBtn.addEventListener('click', () => {
        if (historyStack.length > 0) {
            historyStack.pop();
            if (historyStack.length > 0) {
                resultImg.src = historyStack[historyStack.length - 1];
            } else {
                resultImg.style.display = 'none';
                resultPlaceholder.style.display = 'flex';
            }
            updateUndoButton();
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
            alert('Lütfen önce birinci görüntüyü yükleyin!');
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
                    alert('Hata: ' + data.message);
                }
            } catch (error) {
                alert('Sunucuya bağlanılamadı.');
            } finally {
                histogramLoader.style.display = 'none';
            }
            return;
        }

        if (currentOperation.startsWith('arithmetic') && !file2.files[0]) {
            alert('Bu işlem için ikinci görüntüyü yüklemeniz gereklidir!');
            return;
        }

        const formData = new FormData();
        formData.append('file1', currentFile);
        if (file2.files[0]) {
            formData.append('file2', file2.files[0]);
        }
        formData.append('operation', currentOperation);
        
        // Append dynamic slider params
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
                alert('Hata: ' + data.message);
                if (historyStack.length > 0) resultImg.style.display = 'block';
                else resultPlaceholder.style.display = 'flex';
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Sunucuya bağlanılamadı.');
            if (historyStack.length > 0) resultImg.style.display = 'block';
            else resultPlaceholder.style.display = 'flex';
        } finally {
            loader.style.display = 'none';
            processBtn.disabled = false;
        }
    });
});
