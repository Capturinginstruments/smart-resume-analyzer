/* ====================================================
   SMART RESUME ANALYZER - JAVASCRIPT
   Drag-and-Drop, File Selection Preview, & UI Handlers
   ==================================================== */

document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('resumeInput');
    const fileInfoCard = document.getElementById('fileInfoCard');
    const fileNameDisplay = document.getElementById('fileNameDisplay');
    const fileMetaDisplay = document.getElementById('fileMetaDisplay');
    const removeFileBtn = document.getElementById('removeFileBtn');
    const uploadForm = document.getElementById('uploadForm');

    if (dropZone && fileInput) {
        // Trigger file picker click when dropzone clicked
        dropZone.addEventListener('click', (e) => {
            // Avoid double trigger if remove button or input itself clicked
            if (e.target !== removeFileBtn && !removeFileBtn.contains(e.target)) {
                fileInput.click();
            }
        });

        // Drag & Drop event listeners
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.remove('dragover');
            }, false);
        });

        // Handle File Drop
        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files && files.length > 0) {
                fileInput.files = files;
                handleFileSelect(files[0]);
            }
        });

        // Handle File Input Change
        fileInput.addEventListener('change', (e) => {
            if (fileInput.files && fileInput.files.length > 0) {
                handleFileSelect(fileInput.files[0]);
            }
        });

        // Remove File Handler
        if (removeFileBtn) {
            removeFileBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                fileInput.value = '';
                if (fileInfoCard) {
                    fileInfoCard.style.display = 'none';
                }
            });
        }
    }

    function handleFileSelect(file) {
        if (!fileInfoCard || !fileNameDisplay || !fileMetaDisplay) return;

        const maxSizeBytes = 5 * 1024 * 1024; // 5 MB
        const allowedExts = ['pdf', 'docx', 'doc', 'jpg', 'jpeg', 'png'];
        const ext = file.name.split('.').pop().toLowerCase();

        // Client-side validation
        if (file.size > maxSizeBytes) {
            alert('File size exceeds 5 MB. Please select a smaller file.');
            fileInput.value = '';
            fileInfoCard.style.display = 'none';
            return;
        }

        if (!allowedExts.includes(ext)) {
            alert('Unsupported file format. Please upload PDF, DOCX, JPG, JPEG, or PNG.');
            fileInput.value = '';
            fileInfoCard.style.display = 'none';
            return;
        }

        // Format file size
        let sizeStr = '';
        if (file.size < 1024 * 1024) {
            sizeStr = (file.size / 1024).toFixed(1) + ' KB';
        } else {
            sizeStr = (file.size / (1024 * 1024)).toFixed(2) + ' MB';
        }

        fileNameDisplay.textContent = file.name;
        fileMetaDisplay.textContent = `${ext.toUpperCase()} File • ${sizeStr}`;
        fileInfoCard.style.display = 'flex';
    }
});
