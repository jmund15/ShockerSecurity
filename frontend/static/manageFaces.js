//const imageUrl = "{{ url_for('static', filename='faceImages/') }}"
//const base64Src = `data:image/jpeg;base64,`; // (+${face.face}) Adjust the MIME type if necessary


let data = []; // Declare data as a global variable
let facesToDelete = []; // Array to store IDs of faces marked for deletion
let applyChangeButton;
let csrfToken;

document.addEventListener('DOMContentLoaded', () => {
    csrfToken = document.querySelector('input[name="csrf_token"]').value;
    console.log(csrfToken);
    applyChangeButton = document.getElementById('applyChangesButton');
    applyChangeButton.addEventListener('submit', updateAllFaces);
    
});

// Fetch data from the SQLite database
function fetchFacesData() {
    fetch(faceDataUrl)
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
            <td><img src="${imageUrl + face.face}" alt="${face.name}" style="width: 50px; height: auto;"></td>
            <td><button class="deleteButton" data-id="${face.id}">Toggle Delete</button></td>`
        ;
       
        tableBody.appendChild(row);

        // Add event listeners for input changes
        row.querySelector('input[type="text"]').addEventListener('input', applyButtonCheck);
        row.querySelector('input[type="checkbox"]').addEventListener('change', applyButtonCheck);
        row.querySelector('.deleteButton').addEventListener('click', () => markForDeletion(face.id));
        row.querySelector('.deleteButton').addEventListener('click', applyButtonCheck);
    });

    applyButtonCheck(); // Initial check to disable/enable button
}

function applyButtonCheck() {
    if (facesToDelete.length != 0) {
        applyChangeButton.disabled = false;
    }
    else {
        const rows = document.querySelectorAll('#facesTable tbody tr');
        const hasChanges = Array.from(rows).some(row => {
            const id = row.querySelector('input[data-id]').dataset.id;
            const name = row.querySelector('input[type="text"]').value;
            const accepted = row.querySelector('input[type="checkbox"]').checked;
    
            const originalFace = data.find(face => face.id == id); // Use the original data
            //console.log ("original name: " + originalFace.name + "- curr name: " + name);
            //console.log ("original accepted: " + originalFace.accepted + "- curr accepted: " + accepted);
            return originalFace.name !== name || !!originalFace.accepted !== !!accepted;
        });
        applyChangeButton.disabled = !hasChanges;
    }
    
}

function markForDeletion(id) {
    const row = document.querySelector(`button[data-id="${id}"]`).closest('tr');

    if (!facesToDelete.includes(id)) {
        facesToDelete.push(id);
        row.querySelector('input[data-id]').classList.add('deleting');
        row.querySelector('input[type="text"]').classList.add('deleting');
        row.querySelector('input[type="checkbox"]').classList.add('deleting');
        row.querySelector('img').classList.add('deleting');
        row.classList.add('deleting-row'); // Add class for greying out
    } else {
        facesToDelete = facesToDelete.filter(faceId => faceId !== id);
        row.querySelector('input[data-id]').classList.remove('deleting');
        row.querySelector('input[type="text"]').classList.remove('deleting');
        row.querySelector('input[type="checkbox"]').classList.remove('deleting');
        row.querySelector('img').classList.remove('deleting');
        row.classList.remove('deleting-row'); // Remove class to restore
    }
    //console.log(`Face ID ${id} toggled deletion.`);
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

function updateAllFaces(event) {
    event.preventDefault();

    const rows = document.querySelectorAll('#facesTable tbody tr');
    const promises = []; // Array to hold promises for concurrent execution

    rows.forEach(row => {
        const id = row.querySelector('input[data-id]').dataset.id;
        const name = row.querySelector('input[type="text"]').value;
        const accepted = row.querySelector('input[type="checkbox"]').checked;

        console.log("calling post with csrf token: " + csrfToken);
        // Check if this face is marked for deletion
        if (facesToDelete.includes(parseInt(id))) {
            const deleteData = { id: parseInt(id) };
            console.log(JSON.stringify(deleteData)); // Log the delete request body
            const deletePromise = fetch(deleteUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': csrfToken,
                },
                body: JSON.stringify(deleteData),
            });

            promises.push(deletePromise);
        }
        else {
            // Update face data
            const updateData = { id: parseInt(id), name, accepted };
            console.log(JSON.stringify(updateData)); // Log the delete request body
            const updatePromise = fetch(updateUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': csrfToken,
                },
                body: JSON.stringify(updateData),
            });
            promises.push(updatePromise);
        }
    });

    // Execute all promises
    Promise.all(promises)
        .then(results => {
            console.log(results);
            alert('All faces updated and deletions processed!');
            fetchFacesData(); // Refresh the table
            facesToDelete = []; // Clear the deletion array
        })
        .catch(error => console.error('Error updating or deleting data:', error));
}

console.log("Loading inital data...");
// Load initial data
fetchFacesData();