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