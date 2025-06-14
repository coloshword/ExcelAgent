### frontend.py: module for the frontend code
import webview

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sleek Upload Area</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            background-color: #f3f4f6; /* Light gray background for the page */
            margin: 0;
            padding: 1rem;
        }

        .upload-area {
            transition: all 0.3s ease-in-out;
            /* Base styles for the upload area */
        }

        .upload-area.drag-over {
            border-color: #2563eb; /* Blue-600 */
            background-color: #eff6ff; /* Blue-50 */
            transform: scale(1.02); /* Slight zoom effect */
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3); /* Blue glow */
        }

        .upload-area.drag-over .upload-icon svg {
            transform: scale(1.1) translateY(-5px);
        }

        .upload-icon svg {
            transition: transform 0.3s ease-in-out;
        }

        /* Style for the hidden file input */
        #fileInput {
            display: none;
        }
    </style>
</head>
<body class="bg-slate-100">

    <div id="uploadContainer" class="w-full max-w-lg p-4">
        <label for="fileInput" id="dropZone"
            class="upload-area flex flex-col items-center justify-center w-full h-64
                   border-2 border-dashed border-slate-300 rounded-xl
                   cursor-pointer bg-white hover:bg-slate-50
                   transition-colors duration-300 ease-in-out">

            <div class="upload-icon mb-4 text-slate-400">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
            </div>

            <div class="text-center">
                <p class="text-xl font-semibold text-slate-700">
                    Drag & Drop files here
                </p>
                <p class="text-sm text-slate-500 mt-1">
                    or <span class="font-medium text-blue-600 hover:text-blue-700">click to browse</span>
                </p>
                <p class="text-xs text-slate-400 mt-3">
                    Supports: JPG, PNG, PDF, MP4 (Max 10MB)
                </p>
            </div>
        </label>

        <input type="file" id="fileInput" multiple>

        <div id="filePreview" class="mt-6 space-y-2">
            </div>

        <div id="messageArea" class="mt-4 text-center">
            </div>
    </div>

    <script>
        const dropZone = document.getElementById('dropZone');
        const fileInput = document.getElementById('fileInput');
        const filePreview = document.getElementById('filePreview');
        const messageArea = document.getElementById('messageArea');

        async function toB64(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = () => resolve(reader.result);
                reader.onerror = error => reject(error);
            });
        }

        // Function to be called when files are selected/dropped
        async function handleFiles(files) {
            console.log('Files selected:', files);
            messageArea.innerHTML = ''; // Clear previous messages
            filePreview.innerHTML = ''; // Clear previous previews

            if (files.length === 0) {
                messageArea.innerHTML = '<p class="text-sm text-slate-500">No files selected.</p>';
                return;
            }

            // Example: Display file names and a success message
            let fileListHTML = '<h3 class="text-md font-semibold text-slate-700 mb-2">Selected Files:</h3><ul class="list-disc list-inside text-sm text-slate-600">';
            for (let i = 0; i < files.length; i++) {
                fileListHTML += `<li>${files[i].name} (${(files[i].size / 1024).toFixed(2)} KB)</li>`;
            }
            fileListHTML += '</ul>';
            filePreview.innerHTML = fileListHTML;

            // You would typically start the upload process here.
            // For now, just a log and a message.
            messageArea.innerHTML = '<p class="text-green-600 font-medium">Files ready for upload (simulated).</p>';

            // Example of calling your actual upload function:
            const b64 = await toB64(files[0]);
            const result = await pywebview.api.add_dataframe(b64);
        }

        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false); // Prevent browser from opening file on accidental drop outside zone
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        // Highlight drop zone when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });


        function highlight(e) {
            dropZone.classList.add('drag-over');
            // Change icon color or other elements if needed
            const icon = dropZone.querySelector('.upload-icon svg');
            if (icon) {
                icon.classList.remove('text-slate-400');
                icon.classList.add('text-blue-500');
            }
        }

        function unhighlight(e) {
            dropZone.classList.remove('drag-over');
            const icon = dropZone.querySelector('.upload-icon svg');
            if (icon) {
                icon.classList.remove('text-blue-500');
                icon.classList.add('text-slate-400');
            }
        }

        // Handle dropped files
        dropZone.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            handleFiles(files); // Call your function
            fileInput.files = files; // Optional: if you want the input to also hold the dropped files
        }

        // Handle click to open file dialog
        dropZone.addEventListener('click', () => {
            fileInput.click();
        });

        // Handle file selection from dialog
        fileInput.addEventListener('change', function(e) {
            handleFiles(this.files); // Call your function
        });

    </script>

</body>
</html>
"""
