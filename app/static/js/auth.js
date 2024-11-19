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

function showImage(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.getElementById('profile-pic');
            img.src = e.target.result;
            img.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

function validateForm() {
    const profilePicture = document.getElementById("profile-picture");
    const profileError = document.getElementById("profile-error");
    const password = document.getElementById("password");
    const rePassword = document.getElementById("re-password");
    if (!profilePicture.files.length) {
        profileError.style.display = "block";
        return false;
    }
    if(password != rePassword) {
        return false;
    }
    profileError.style.display = "none";
    return true;

}