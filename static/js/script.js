document.addEventListener("DOMContentLoaded", () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    let selectedFile = null;

    // Toast Utility
    window.copyData = function(text) {
        navigator.clipboard.writeText(text);
        const toast = document.getElementById("toast");
        toast.className = "show";
        setTimeout(() => { toast.className = toast.className.replace("show", ""); }, 2900);
    }

    if (dropZone && fileInput) {
        // Drag and Drop Logic
        dropZone.addEventListener('click', () => fileInput.click());
        dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('dragover'); });
        dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault(); dropZone.classList.remove('dragover');
            if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
        });

        fileInput.addEventListener('change', function() {
            if (this.files.length) handleFile(this.files[0]);
        });

        function handleFile(file) {
            selectedFile = file;
            dropZone.innerHTML = `<p style="color:var(--primary); font-weight:600;">📁 ${file.name}</p><p style="font-size:12px; margin-top:8px;">Ready to encrypt</p>`;
        }

        // Upload Logic
        uploadBtn.addEventListener('click', function() {
            if (!selectedFile) { alert("Please select a file."); return; }

            const btn = this;
            const progressContainer = document.getElementById('progressContainer');
            const progressBar = document.getElementById('progressBar');
            const resultBox = document.getElementById('resultBox');
            
            btn.disabled = true;
            btn.innerText = "Encrypting Payload...";
            progressContainer.style.display = 'block';
            progressBar.style.width = '0%';
            resultBox.style.display = 'none';

            const formData = new FormData();
            formData.append('file', selectedFile);

            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/upload', true);

            xhr.upload.onprogress = function(e) {
                if (e.lengthComputable) {
                    progressBar.style.width = (e.loaded / e.total) * 100 + '%';
                }
            };

            xhr.onload = function() {
                btn.disabled = false;
                btn.innerText = "Encrypt & Generate Access";
                progressContainer.style.display = 'none';
                
                if (xhr.status === 200) {
                    const data = JSON.parse(xhr.responseText);
                    document.getElementById('outLink').innerText = data.link;
                    document.getElementById('outKey').innerText = data.key;
                    
                    // AI Heuristic Display
                    document.getElementById('aiRisk').innerHTML = `AI Scan: <span style="color:${data.risk_profile.color}; font-weight:bold;">${data.risk_profile.status} (Score: ${data.risk_profile.risk_score})</span>`;

                    // Generate QR
                    document.getElementById('qrcode').innerHTML = ""; 
                    new QRCode(document.getElementById("qrcode"), {
                        text: data.link, width: 120, height: 120,
                        colorDark : "#0f172a", colorLight : "#ffffff"
                    });

                    resultBox.style.display = 'block';
                    selectedFile = null;
                    dropZone.innerHTML = `<p>Drag & drop a payload here, or <strong style="color:var(--primary)">browse</strong></p>`;
                } else {
                    alert("Encryption Failed. Max size is 50MB.");
                }
            };

            xhr.send(formData);
        });
    }
});