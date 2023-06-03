document.addEventListener('DOMContentLoaded', () => {
    const uploadDrop = document.querySelector('.upload-drop');
    const uploadInput = document.getElementById('upload');

    // Handle file drop
    uploadDrop.addEventListener('drop', (event) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('upload', event.dataTransfer.files[0]);
    });

    // Prevent default behavior when file is dragged over uploadDrop
    uploadDrop.addEventListener('dragover', (event) => {
        event.preventDefault();
    });

    // Function to handle file upload
    const handleFileUpload = (file) => {
        const formData = new FormData();
        formData.append('upload', file);

        // Send file to server
        fetch('/upload/sketch', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                Swal.fire({
                    icon: 'success',
                    title: 'Success',
                    text: 'Gambar berhasil diupload!',
                    showClass: {
                        popup: 'animate__animated animate__bounceIn'
                    },
                    hideClass: {
                        popup: 'animate__animated animate__bounceOut'
                    }
                }).then(() => {
                    window.location.href = '/uploaded_sketch';
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Terjadi kesalahan saat upload gambar. Pastikan mengupload dengan format yang diizinkan (png, jpg, atau jpeg)',
                    showClass: {
                        popup: 'animate__animated animate__fadeInDown'
                    },
                    hideClass: {
                        popup: 'animate__animated animate__fadeOutDown'
                    }
                });
            }
        });
    };

    // Function to handle file drop
    const handleFileDrop = (event) => {
        event.preventDefault();
        const file = event.dataTransfer.files[0];
        handleFileUpload(file);
    };

    // Event listeners for file selection and drop
    uploadInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        handleFileUpload(file);
    });

    uploadDrop.addEventListener('dragover', (event) => {
        event.preventDefault();
        uploadDrop.classList.add('drag-over');
    });

    uploadDrop.addEventListener('dragleave', () => {
        uploadDrop.classList.remove('drag-over');
    });

    uploadDrop.addEventListener('drop', handleFileDrop);
});
