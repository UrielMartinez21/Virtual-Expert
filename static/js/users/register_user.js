document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("register-form");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        // Create a FormData object from the form
        const formData = new FormData(form);

        // Get data from the form
        const username = formData.get("username");
        const firstName = formData.get("first_name");
        const lastName = formData.get("last_name");
        const email = formData.get("email");
        const password = formData.get("password");
        const confirmPassword = formData.get("confirm_password");

        // Validations
        if (!username) {
            alert("User is required.");
            return;
        }
        if (!firstName) {
            alert("First name is required.");
            return;
        }
        if (!lastName) {
            alert("Last name is required.");
            return;
        }
        if (!email) {
            alert("Email is required.");
            return;
        }
        if (!/\S+@\S+\.\S+/.test(email)) {
            alert("Email is invalid.");
            return;
        }
        if (!password) {
            alert("Password is required.");
            return;
        }
        if (!confirmPassword) {
            alert("Confirm password is required.");
            return;
        }
        if (username.length < 3 || username.length > 20) {
            alert("Username must be between 3 and 20 characters long.");
            return;
        }
        if (!/^[a-zA-Z0-9_]+$/.test(username)) {
            alert("Username can only contain letters, numbers, and underscores.");
            return;
        }
        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }
        if (password.length < 6) {
            alert("Password must be at least 6 characters long.");
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
                title: 'Login Successful',
                text: 'Welcome back!',
                icon: 'success',
                confirmButtonText: 'Continue'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = "/";
                }
            });
        } else {
            alert("Error: " + (result.message));
        }
    });
});
