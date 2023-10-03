document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");
    const tokenDisplay = document.getElementById("token-display");

    loginForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            const token = await getToken(email, password);
            localStorage.setItem("authToken", token);
            tokenDisplay.innerHTML = `Bearer Token: ${token}`;
        } catch (error) {
            console.error("Login failed:", error.message);
        }
    });

    async function getToken(email, password) {
        const apiUrl = "http://127.0.0.1:8000/api/v1/users/login"; // Replace with your API URL

        // Create URL-encoded data
        const formData = new URLSearchParams();
        formData.append("username", email);
        formData.append("password", password);

        const response = await fetch(apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: formData.toString(), // Convert the URLSearchParams object to a string
        });

        if (!response.ok) {
            throw new Error("Login failed");
        }


        const data = await response.json();
        localStorage.setItem("accessToken", data.access_token);


        const categoryName = "New Category";
        try {
            const result = await createCategory(categoryName);
            console.log("Category created successfully:", result);
        } catch (error) {
            console.error("Error creating category:", error.message);
        }


        return data.access_token;
    }
});

async function createCategory(categoryName) {
    const apiUrl = "http://127.0.0.1:8000/api/v1/posts/categories"; // Replace with your API URL

    // Create JSON data
    const jsonData = {
        name: categoryName,
    };

    const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("accessToken")}`
        },
        body: JSON.stringify(jsonData),
    });

    if (!response.ok) {
        throw new Error("Category creation failed");
    }

    const data = await response.json();
    return data; // You might want to return some useful information here
}

// Example usage

