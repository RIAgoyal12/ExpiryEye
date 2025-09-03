
function handleLogin(event) {
    event.preventDefault();

    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;

    // Retrieve the user data from localStorage
    const userData = JSON.parse(localStorage.getItem("user"));

    // Validate the login credentials
    if (userData && userData.email === username && userData.password === password) {
        alert("Login successful!");
        window.location.href = "home.html"; // Redirect to the main page
    } else {
        alert("Invalid credentials. Please try again.");
    }
}
