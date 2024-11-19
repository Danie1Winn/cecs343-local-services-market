// Function to switch tabs between Worker and Employer forms
function showTab(tabName) {
    const employerForm = document.getElementById('employerForm');
    const workerForm = document.getElementById('workerForm');
    const employerTab = document.getElementById('employerTab');
    const workerTab = document.getElementById('workerTab');

    if (tabName === 'employer') {
        employerForm.style.display = 'block';
        workerForm.style.display = 'none';
        employerTab.classList.add('active');
        workerTab.classList.remove('active');
    } else {
        employerForm.style.display = 'none';
        workerForm.style.display = 'block';
        workerTab.classList.add('active');
        employerTab.classList.remove('active');
    }
}

// Function to display the selected profile picture for Worker form
function showImage(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const img = document.getElementById('profile-pic');
            img.src = e.target.result;
            img.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

// Validation for Worker form
function validateWorkerForm(event) {
    const profilePicture = document.getElementById("profile-picture");
    const profileError = document.getElementById("profile-error");
    const password = document.getElementById("workerPassword");
    const rePassword = document.getElementById("workerRe-Password");
    const passwordError = document.getElementById("worker-password-error");

    let isValid = true;

    // Check if profile picture is uploaded
    if (!profilePicture.files.length) {
        profileError.style.display = "block";
        isValid = false;
    } else {
        profileError.style.display = "none";
    }

    // Check if passwords match
    if (password.value !== rePassword.value) {
        passwordError.style.display = "block";
        rePassword.classList.add("error-highlight");
        isValid = false;
    } else {
        passwordError.style.display = "none";
        rePassword.classList.remove("error-highlight");
    }

    // Prevent form submission if invalid
    if (!isValid) {
        event.preventDefault();
    }

    return isValid;
}

// Validation for Employer form
function validateEmployerForm(event) {
    const password = document.getElementById("employerPassword");
    const rePassword = document.getElementById("employerRe-Password");
    const passwordError = document.getElementById("password-error");

    let isValid = true;

    // Check if passwords match
    if (password.value !== rePassword.value) {
        passwordError.style.display = "block";
        rePassword.classList.add("error-highlight");
        isValid = false;
    } else {
        passwordError.style.display = "none";
        rePassword.classList.remove("error-highlight");
    }

    // Prevent form submission if invalid
    if (!isValid) {
        event.preventDefault();
    }

    return isValid;
}