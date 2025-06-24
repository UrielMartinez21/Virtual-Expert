document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        // Create a FormData object from the form
        const formData = new FormData(form);

        // Get data from the form
        const username = formData.get("username");
        const password = formData.get("password");

        // Validations
        if (!username) {
            alert("User is required.");
            return;
        }
        if (!password) {
            alert("Password is required.");
            return;
        }

        // Send the form data to the server
        const response = await fetch(form.action, {
            method: "POST",
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            alert("Ok: " + result.message);                 // Show success message
            window.location.href = "/users/dashboard/";     // Redirect to dashboard on success
        } else {
            alert("Error: " + (result.message));
        }
    });
});
