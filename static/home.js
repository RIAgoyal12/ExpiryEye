
   function switchMethod(method) {
            document.querySelectorAll('.input-section').forEach(section => section.style.display = 'none');
            document.getElementById(`${method}-section`).style.display = 'block';
        }
        window.onload = () => switchMethod('upload');

        const fileInput = document.getElementById('file-input');

        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                alert(`File ${file.name} is ready for upload.`);
            }
        });

        function submitDetails() {
            const name = document.getElementById('product-name').value;
            const expiryDate = document.getElementById('expiry-date').value;
            const batchNumber = document.getElementById('batch-number').value;

            if (name && expiryDate && batchNumber) {
                alert('Details submitted successfully!');
            } else {
                alert('Please fill in all fields.');
            }
        }
    