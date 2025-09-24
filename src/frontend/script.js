document.addEventListener('DOMContentLoaded', () => {
    // Elementos da interface
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const progressBar = document.getElementById('progressBar');
    const progress = document.getElementById('progress');
    const resultsSection = document.getElementById('resultsSection');
    const jsonViewer = document.getElementById('jsonViewer');
    const downloadJson = document.getElementById('downloadJson');
    const loadingOverlay = document.getElementById('loadingOverlay');

    // Reset do estado inicial
    const resetUI = () => {
        progressBar.style.display = 'none';
        loadingOverlay.hidden = true;
        resultsSection.hidden = true;
        dropZone.style.display = 'block';
    };

    // Inicializar interface
    resetUI();

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop zone when dragging over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    // Handle dropped files
    dropZone.addEventListener('drop', handleDrop, false);
    fileInput.addEventListener('change', handleFileSelect, false);

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight(e) {
        dropZone.classList.add('drag-over');
    }

    function unhighlight(e) {
        dropZone.classList.remove('drag-over');
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    function handleFileSelect(e) {
        const files = e.target.files;
        handleFiles(files);
    }

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (file.type === 'application/pdf') {
                uploadFile(file);
            } else {
                alert('Por favor, selecione um arquivo PDF.');
            }
        }
    }

    async function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        progressBar.style.display = 'block';
        loadingOverlay.hidden = false;

        try {
            const response = await fetch('http://localhost:8000/api/v1/contracts/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            displayResults(result);
        } catch (error) {
            console.error('Error:', error);
            alert('Erro ao processar o arquivo. Por favor, tente novamente.');
        } finally {
            loadingOverlay.hidden = true;
            progressBar.style.display = 'none';
        }
    }

    function displayResults(data) {
        resultsSection.hidden = false;
        jsonViewer.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
        
        downloadJson.onclick = () => {
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'analise-contrato.json';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        };
    }
});