document.addEventListener("DOMContentLoaded", function () {
    // Handling form submission for login
    const loginForm = document.getElementById("loginform");
    if (loginForm) {
        loginForm.addEventListener("submit", async function (event) {
            event.preventDefault(); // Prevent the default form submission

            const username = document.getElementById("login-username").value;
            const password = document.getElementById("login-password").value;

            // Create a JSON object with the username and password
            const data = {
                username: username,
                password: password
            };

            try {
                const response = await fetch("/", {
                    method: "POST",
                    body: JSON.stringify(data),  // Send data as a JSON string
                    headers: {
                        "Accept": "application/json",  // Ensure response is JSON
                        "Content-Type": "application/json"  // Set the correct content type for JSON
                    }
                });

                const result = await response.json();  // Parse JSON response

                if (response.ok) {
                    // Handle successful login
                    alert("Login successful! Redirecting...");
                    window.location.href = "/index";  // Redirect to index page after login
                } else {
                    // Handle error
                    alert(result.message || "Login failed, please try again.");
                }
            } catch (error) {
                console.error("Error during login:", error);
                alert("An error occurred. Please try again.");
            }
        });
    }

    // Handling form submission for registration
    const registerForm = document.getElementById("register-form");
    if (registerForm) {
        registerForm.addEventListener("submit", async function (event) {
            event.preventDefault(); // Prevent the default form submission

            const username = document.getElementById("register-username").value;
            const password = document.getElementById("register-password").value;

            // Create a JSON object with the username and password
            const data = {
                username: username,
                password: password
            };

            try {
                const response = await fetch("/register", {
                    method: "POST",
                    body: JSON.stringify(data),  // Send data as a JSON string
                    headers: {
                        "Accept": "application/json",  // Ensure response is JSON
                        "Content-Type": "application/json"  // Set the correct content type for JSON
                    }
                });

                const result = await response.json();  // Parse JSON response

                if (response.ok) {
                    // Handle successful registration
                    alert("Registration successful! Please log in.");
                    window.location.href = "/";  // Redirect to login page after registration
                } else {
                    // Handle error
                    alert(result.message || "Registration failed, please try again.");
                }
            } catch (error) {
                console.error("Error during registration:", error);
                alert("An error occurred. Please try again.");
            }
        });
    }
});