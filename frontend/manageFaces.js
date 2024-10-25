const apiUrl = 'http://localhost:3000/faces';

let data = []; // Declare data as a global variable
applyChangeButton = document.getElementById('applyChangesButton')
applyChangeButton.onclick = updateAllFaces;

// Fetch data from the SQLite database
function fetchFacesData() {
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => loadTableData(data))
        .catch(error => console.error('Error fetching data:', error));
}

function loadTableData(facesData) {
    data = facesData
    const tableBody = document.querySelector('#facesTable tbody');
    tableBody.innerHTML = ""; // Clear existing data

    data.forEach(face => {
        const row = document.createElement('tr');

        row.innerHTML = `
            <td>${face.id}</td>
            <td><input type="text" value="${face.name}" data-id="${face.id}"></td>
            <td><input type="checkbox" ${face.accepted ? 'checked' : ''} data-id="${face.id}"></td>
            <td><img src="${face.face}" alt="${face.name}" style="width: 50px; height: auto;"></td>
        `;
       
        tableBody.appendChild(row);

        // Add event listeners for input changes
        row.querySelector('input[type="text"]').addEventListener('input', applyButtonCheck);
        row.querySelector('input[type="checkbox"]').addEventListener('change', applyButtonCheck);
    });

    applyButtonCheck(); // Initial check to disable/enable button
}

function applyButtonCheck() {
    const rows = document.querySelectorAll('#facesTable tbody tr');
    const hasChanges = Array.from(rows).some(row => {
        const id = row.querySelector('input[data-id]').dataset.id;
        const name = row.querySelector('input[type="text"]').value;
        const accepted = row.querySelector('input[type="checkbox"]').checked;

        const originalFace = data.find(face => face.id == id); // Use the original data
        return originalFace.name !== name || originalFace.accepted !== accepted;
    });

    applyChangeButton.disabled = !hasChanges;
}

// function updateFace(id) {
//     const row = document.querySelector(`input[data-id="${id}"]`);
//     const name = row.value;
//     const accepted = document.querySelector(`input[type="checkbox"][data-id="${id}"]`).checked;

//     const data = { id, name, accepted };

//     fetch('http://localhost:5000/faces/update', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(data),
//     })
//     .then(response => response.json())
//     .then(result => {
//         console.log(result);
//         alert(`Face ID ${id} updated!`);
//         fetchFacesData(); // Refresh the table
//     })
//     .catch(error => console.error('Error updating data:', error));
// }

function updateAllFaces() {
    const facesData = [];
    const rows = document.querySelectorAll('#facesTable tbody tr');

    rows.forEach(row => {
        const id = row.querySelector('input[data-id]').dataset.id;
        const name = row.querySelector('input[type="text"]').value;
        const accepted = row.querySelector('input[type="checkbox"]').checked;

        facesData.push({ id: parseInt(id), name, accepted });
    });

    fetch('http://localhost:5000/faces/updateAll', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(facesData),
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        alert('All faces updated!');
        fetchFacesData(); // Refresh the table
    })
    .catch(error => console.error('Error updating data:', error));
}

// Load initial data
fetchFacesData();