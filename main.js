
/* =========================
   SEU Volunteering Platform
   Main JavaScript
========================= */


/* =========================
   PAGE LOADED CHECK
========================= */
document.addEventListener("DOMContentLoaded", function () {
    console.log("SEU Volunteering Platform Loaded 🚀");
});


/* =========================
   LOGIN FUNCTION
========================= */
function loginUser(event) {
    event.preventDefault();

    let email = document.getElementById("email");
    let password = document.getElementById("password");

    if (email.value === "" || password.value === "") {
        alert("Please fill all fields");
        return false;
    }

    // Fake login (for frontend only)
    alert("Login Successful 🚀");

    // redirect to dashboard
    window.location.href = "student-dashboard.html";

    return false;
}


/* =========================
   REGISTER FUNCTION
========================= */
function registerUser(event) {
    event.preventDefault();

    let name = document.getElementById("name");
    let email = document.getElementById("email");
    let password = document.getElementById("password");
    let role = document.getElementById("role");

    if (
        name.value === "" ||
        email.value === "" ||
        password.value === "" ||
        role.value === ""
    ) {
        alert("Please fill all fields");
        return false;
    }

    alert("Account Created Successfully 🎉");

    // redirect to login page
    window.location.href = "login.html";

    return false;
}


/* =========================
   REGISTER FOR OPPORTUNITY
   (Dashboard Buttons)
========================= */
function registerForOpportunity(button) {
    button.innerHTML = "Registered ✔";
    button.disabled = true;
    button.classList.remove("btn-primary");
    button.classList.add("btn-success");

    alert("You successfully registered for this opportunity!");
}


/* =========================
   SIMPLE UI EFFECT
========================= */
function showMessage(msg) {
    alert(msg);
}