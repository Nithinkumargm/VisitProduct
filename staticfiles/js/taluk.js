document.addEventListener('DOMContentLoaded', function () {
    const employeeSelect = document.getElementById('id_employee');
    const talukSelect = document.getElementById('id_taluk');

    employeeSelect.addEventListener('change', function () {
        const employeeId = employeeSelect.value;
        fetch(`/api/load-taluks/?employee_id=${employeeId}`)
            .then(response => response.json())
            .then(data => {
                talukSelect.innerHTML = '';
                data.forEach(taluk => {
                    const option = document.createElement('option');
                    option.value = taluk.id;
                    option.textContent = taluk.name;
                    talukSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error:', error));
    });
});
