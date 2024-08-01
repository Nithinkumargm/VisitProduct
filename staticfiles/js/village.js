document.addEventListener('DOMContentLoaded', function () {
    const talukSelect = document.getElementById('id_taluk');
    const villageSelect = document.getElementById('id_name'); 

    talukSelect.addEventListener('change', function () {
        const talukId = talukSelect.value;
        fetch(`/api/load-villages/?taluk_id=${talukId}`)
            .then(response => response.json())
            .then(data => {
                villageSelect.innerHTML = '';
                data.forEach(village => {
                    const option = document.createElement('option');
                    option.value = village.id;
                    option.textContent = village.name;
                    villageSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error:', error));
    });
});
