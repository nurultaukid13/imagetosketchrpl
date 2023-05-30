document.addEventListener('DOMContentLoaded', () => {
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
                alert('Terjadi kesalahan saat upload gambar. Pastikan mengupload dengan format yang diizinkan (png, jpg atau jpeg) dan ukuran dibawah 10MB');
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
                    text: 'Terjadi kesalahan saat upload gambar. Pastikan mengupload dengan format yang diizinkan (png, jpg, atau jpeg) dan ukuran dibawah 10MB',
                    showClass: {
                        popup: 'animate__animated animate__flipInY'
                      },
                      hideClass: {
                        popup: 'animate__animated animate__flipOutY'
                      }
                });
            }
        });
    });
});
