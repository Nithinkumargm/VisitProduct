document.addEventListener('DOMContentLoaded', function () {
    const employeeSelect = document.getElementById('id_employee');
    const talukSelect = document.getElementById('id_taluk');
    const villageSelect = document.getElementById('id_village');
    const dairySelect = document.getElementById('id_dairy');  // Ensure this ID matches the form field

    function updateVillageDropdown(villages) {
        villageSelect.innerHTML = '<option value="">---------</option>';  // Clear existing options
        villages.forEach(village => {
            const option = document.createElement('option');
            option.value = village.id;
            option.textContent = village.name;
            villageSelect.appendChild(option);
        });
    }

    function updateDairyDropdown(dairies) {
        dairySelect.innerHTML = '<option value="">---------</option>';  // Clear existing options
        dairies.forEach(dairy => {
            const option = document.createElement('option');
            option.value = dairy.id;
            option.textContent = dairy.name;
            dairySelect.appendChild(option);
        });
    }

    employeeSelect.addEventListener('change', function () {
        const employeeId = employeeSelect.value;
        fetch(`/api/load-taluks/?employee_id=${employeeId}`)
            .then(response => response.json())
            .then(data => {
                talukSelect.innerHTML = '<option value="">---------</option>';
                data.forEach(taluk => {
                    const option = document.createElement('option');
                    option.value = taluk.id;
                    option.textContent = taluk.name;
                    talukSelect.appendChild(option);
                });
                talukSelect.dispatchEvent(new Event('change'));  // Trigger taluk change event
            })
            .catch(error => console.error('Error:', error));
    });

    talukSelect.addEventListener('change', function () {
        const talukId = talukSelect.value;
        fetch(`/api/load-villages/?taluk_id=${talukId}`)
            .then(response => response.json())
            .then(data => {
                updateVillageDropdown(data);
                villageSelect.dispatchEvent(new Event('change'));  // Trigger village change event
            })
            .catch(error => console.error('Error:', error));
    });

    villageSelect.addEventListener('change', function () {
        const villageId = villageSelect.value;
        fetch(`/api/load-dairies/?village_id=${villageId}`)
            .then(response => response.json())
            .then(data => {
                updateDairyDropdown(data);
            })
            .catch(error => console.error('Error:', error));
    });
});
