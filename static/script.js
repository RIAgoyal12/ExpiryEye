// // script.js

// // JavaScript function to validate the date format
// function validateDateFormat() {
//     const dateInput = document.getElementById('expiryDate').value;
//     const datePattern = /^(\d{2})\/(\d{2})\/(\d{4})$/; // Regex for dd/mm/yyyy

//     if (!datePattern.test(dateInput)) {
//         alert("Invalid expiry date format. Please use dd/mm/yyyy.");
//         return false; // Prevent form submission
//     }

//     // Check if the date is valid
//     const [day, month, year] = dateInput.split('/');
//     const date = new Date(`${year}-${month}-${day}`);
//     if (date.getDate() != day || date.getMonth() + 1 != month || date.getFullYear() != year) {
//         alert("Invalid date. Please check the day, month, and year.");
//         return false;
//     }

//     return true;
// }

<script>
function switchMethod(method) {
    document.querySelectorAll('.input-section').forEach(section => section.style.display = 'none');
    document.getElementById(`${method}-section`).style.display = 'block';
}
window.onload = () => switchMethod('upload');
</script>


