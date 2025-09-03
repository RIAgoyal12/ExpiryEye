document.getElementById("contact-form").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent the default form submission

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const message = document.getElementById("message").value;

    if (!name || !email || !message) {
        alert("Please fill out all fields!");
        return;  // Stop form submission if fields are empty
    }

    // Simulating form submission (you can remove the next line if you don't need this)
    alert(`Thank you, ${name}! Your message has been sent successfully.`);

    // Reset the form after submission
    document.getElementById("contact-form").reset();
});
