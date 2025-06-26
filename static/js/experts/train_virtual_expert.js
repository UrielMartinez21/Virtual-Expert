document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("train-form");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const slugInput = form.querySelector('input[name="slug"]');
        const fileInput = form.querySelector('input[name="document"]');
        const file = fileInput.files[0];

        // Validations 
        if (!file) {
            Swal.fire({
                icon: 'error',
                title: 'No file selected',
                text: 'Please select a PDF file to upload.',
            });
            return;
        }
        if (!/\.(pdf)$/i.test(file.name)) {
            Swal.fire({
                icon: 'error',
                title: 'Invalid file',
                text: 'Please upload a PDF file only.',
            });
            return;
        }
        // Validate slug
        if (!slugInput) {
            Swal.fire({
                icon: 'error',
                title: 'Missing slug',
                text: 'Slug input is required.',
            });
            return;
        }

        // Confirm upload
        const confirm = await Swal.fire({
            title: 'Train Expert',
            text: `Are you sure you want to train this expert with "${file.name}"?`,
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'Yes, upload and train',
            cancelButtonText: 'Cancel'
        });

        if (!confirm.isConfirmed) return;

        // Show loading
        Swal.fire({
            title: 'Uploading...',
            text: 'Training in progress. Please wait.',
            allowOutsideClick: false,
            didOpen: () => Swal.showLoading()
        });

        // Submit the form manually with fetch
        const formData = new FormData(form);
        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
            });
            
            const result = await response.json();

            if (response.ok) {
                Swal.fire({
                    title: 'Success',
                    text: 'Virtual expert trained successfully!',
                    icon: 'success',
                    confirmButtonText: 'Continue'
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = "/experts/";
                    }
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: result.message || 'An error occurred while training the expert.',
                });
            }


        } catch (err) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Something went wrong during training.',
            });
        }
    });
});
