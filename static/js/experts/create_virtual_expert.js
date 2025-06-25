document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("expert_form");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        // Create a FormData object from the form
        const formData = new FormData(form);

        // Get data from the form
        const name = formData.get("name");
        const description = formData.get("description");

        // Validations
        if (!name) {
            Swal.fire({
                title: "Error",
                text: "Name is required.",
                icon: "error"
            });
            return;
        }
        if (!description) {
            Swal.fire({
                title: "Error",
                text: "Description is required.",
                icon: "error"
            });
            return;
        }

        // Send the form data to the server
        const response = await fetch(form.action, {
            method: "POST",
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            Swal.fire({
                title: 'Success',
                text: 'Virtual expert created successfully!',
                icon: 'success',
                confirmButtonText: 'Continue'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = "/experts/";
                }
            });
        } else {
            alert("Error: " + (result.message));
        }
    });
});
