document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("create-expert-form");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const name = formData.get("name").trim();
        const description = formData.get("description").trim();

        if (!name || !description) {
            Swal.fire({ icon: 'error', title: 'Please fill all fields' });
            return;
        }

        const response = await fetch(form.action, {
            method: "POST",
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            Swal.fire({
                icon: 'success',
                title: 'Expert Created',
                confirmButtonText: 'OK'
            }).then(() => window.location.reload());
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: result.message || 'Failed to create expert'
            });
        }
    });

    // ===========================| Delete Expert |===========================
    const deleteButtons = document.querySelectorAll(".delete-expert");

    deleteButtons.forEach(button => {
        button.addEventListener("click", async (e) => {
            e.preventDefault();

            const expertSlug = button.dataset.slug;

            const confirm = await Swal.fire({
                title: "Are you sure?",
                text: "This action will permanently delete the expert.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#E74C3C",
                cancelButtonColor: "#6c757d",
                confirmButtonText: "Yes, delete it!",
            });

            if (confirm.isConfirmed) {
                try {
                    const response = await fetch(`/experts/delete/${expertSlug}/`, {
                        method: "DELETE",
                    });

                    if (response.ok) {
                        Swal.fire("Deleted!", "The expert was deleted.", "success").then(() => {
                            location.reload();
                        });
                    } else {
                        Swal.fire("Error", "Could not delete the expert.", "error");
                    }
                } catch (err) {
                    Swal.fire("Error", err.message, "error");
                }
            }
        });
    });

    // ===========================| Edit Expert |===========================
    const editForm = document.getElementById("edit-expert-form");
    const editBtns = document.querySelectorAll(".edit-expert-btn");

    editBtns.forEach(btn => {
        btn.addEventListener("click", () => {
        const slug = btn.dataset.slug;
        const name = btn.dataset.name;
        const description = btn.dataset.description;

        editForm.elements["slug"].value = slug;
        editForm.elements["name"].value = name;
        editForm.elements["description"].value = description;
        });
    });

    editForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(editForm);
        const slug = formData.get("slug");

        const response = await fetch(`/experts/update/${slug}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        },
        body: formData
        });

        const result = await response.json();

        if (response.ok) {
        Swal.fire({ icon: 'success', title: 'Expert updated' }).then(() => window.location.reload());
        } else {
        Swal.fire({ icon: 'error', title: 'Update failed', text: result.message || 'Try again' });
        }
    });
});
