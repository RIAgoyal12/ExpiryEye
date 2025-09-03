
    function handleSignup(event) {
      event.preventDefault();

      const fname = document.getElementById("fname").value;
      const lname = document.getElementById("lname").value;
      const email = document.getElementById("uemail").value;
      const password = document.getElementById("pass").value;
      const confirmPassword = document.getElementById("conPass").value;

      // Check if passwords match
      if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return false;
      }

      // Check password length (Password must not exceed 8 characters)
      if (password.length < 8) {
        alert("Password length should not greater than 8 characters.");
        return false;
      }

      // Store user data in localStorage
      localStorage.setItem("user", JSON.stringify({ fname, lname, email, password }));
      alert("Signup successful!");

      // Redirect to homepage after successful signup
      window.location.href = "home.html"; // Redirect to the main page
    }
