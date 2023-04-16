const uploadDrop = document.querySelector('.upload-drop');
const uploadInput = document.getElementById('upload');

// Handle file drop
uploadDrop.addEventListener('drop', (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('upload', event.dataTransfer.files[0]);

    // Send file to server
    fetch('/upload/sketch', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            alert('Gambar berhasil diupload!');
            window.location.href = '/uploaded_sketch';
        } else {
            alert('Terjadi kesalahan saat upload gambar.');
        }
    });
});

// Prevent default behavior when file is dragged over uploadDrop
uploadDrop.addEventListener('dragover', (event) => {
    event.preventDefault();
});

// Handle file selection through uploadInput
uploadInput.addEventListener('change', (event) => {
    const formData = new FormData();
    formData.append('upload', event.target.files[0]);

    // Send file to server
    fetch('/upload/sketch', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            alert('Gambar berhasil diupload!');
            window.location.href = '/uploaded_sketch';
        } else {
            alert('Terjadi kesalahan saat upload gambar.');
        }
    });
});