//const imageUrl = "{{ url_for('static', filename='faceImages/') }}"
//const base64Src = `data:image/jpeg;base64,`; // (+${face.face}) Adjust the MIME type if necessary


let data = []; // Declare data as a global variable
let facesToDelete = []; // Array to store IDs of faces marked for deletion
let applyChangesButton; // This is now the submit button
let applyChangesForm;
let csrfToken;
let hasChanges;

document.addEventListener('DOMContentLoaded', () => {
    csrfToken = document.querySelector('input[name="csrf_token"]').value;
    console.log(csrfToken);
    applyChangesForm = document.getElementById('applyChangesForm');
    applyChangesButton = document.getElementById('applyChangesButton'); // This is now the submit button
    applyChangesForm.addEventListener('submit', function(event) {
        // Show a confirmation dialog
        const discardChanges = confirm("Are you sure you want to apply these changes?");
        if (discardChanges) {
            // If the user confirmed, call the updateAllFaces function
            updateAllFaces(event);
        } else {
            // If the user canceled, prevent the form submission
            event.preventDefault();
        }
    });

    // Confirmation when leaving the page
    window.addEventListener('beforeunload', (event) => {
        if (hasChanges) {
            const confirmationMessage = "You have unsaved changes. Are you sure you want to leave?";
            event.preventDefault(); // This line is needed for some browsers
            return confirmationMessage; // if user canceled, won't exit page
        }
    });
    console.log("Loading inital data...");
    // Load initial data
    fetchFacesData();
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
        // <td><input type="checkbox" ${face.accepted ? 'checked' : ''} data-id="${face.id}"></td>
        row.innerHTML = `
            <td>${face.id}</td>
            <td><input type="text" value="${face.name}" data-id="${face.id}"></td>
            <td>
                <label class="checkbox-container">
                    <input type="checkbox" ${face.accepted ? 'checked' : ''} data-id="${face.id}">
                    <span class="checkmark"></span> <!-- Optional: for styling purposes -->
                </label>
            </td>
            <td><img src="${imageUrl + face.face}" alt="${face.name}'s Image N/A" style="width: 50px; height: auto;"></td>
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
        applyChangesButton.disabled = false;
    }
    else {
        const rows = document.querySelectorAll('#facesTable tbody tr');
        hasChanges = Array.from(rows).some(row => {
            const id = row.querySelector('input[data-id]').dataset.id;
            const name = row.querySelector('input[type="text"]').value;
            const accepted = row.querySelector('input[type="checkbox"]').checked;
    
            const originalFace = data.find(face => face.id == id); // Use the original data
            console.log ("original name: " + originalFace.name + "- curr name: " + name);
            console.log ("original accepted: " + originalFace.accepted + "- curr accepted: " + accepted);
            changesBool = originalFace.name != name || originalFace.accepted != accepted;
            console.log("changes made? : ", changesBool);
            return changesBool;
        });
        applyChangesButton.disabled = !hasChanges;
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
        row.querySelector('button').textContent = "Toggle Undelete";
    } else {
        facesToDelete = facesToDelete.filter(faceId => faceId !== id);
        row.querySelector('input[data-id]').classList.remove('deleting');
        row.querySelector('input[type="text"]').classList.remove('deleting');
        row.querySelector('input[type="checkbox"]').classList.remove('deleting');
        row.querySelector('img').classList.remove('deleting');
        row.classList.remove('deleting-row'); // Remove class to restore
        row.querySelector('button').textContent = "Toggle Delete";
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

async function updateAllFaces(event) {
    event.preventDefault();

    const rows = document.querySelectorAll('#facesTable tbody tr');

    for (const row of rows) {
        const id = row.querySelector('input[data-id]').dataset.id;
        const name = row.querySelector('input[type="text"]').value;
        const accepted = row.querySelector('input[type="checkbox"]').checked;

        console.log("calling post with csrf token: " + csrfToken);
        // Check if this face is marked for deletion
        if (facesToDelete.includes(parseInt(id))) {
            const deleteData = { id: parseInt(id) };
            console.log(JSON.stringify(deleteData)); // Log the delete request body
            await fetch(deleteUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': csrfToken,
                },
                body: JSON.stringify(deleteData),
            });
        } else {
            // Update face data
            const updateData = { id: parseInt(id), name, accepted };
            console.log(JSON.stringify(updateData)); // Log the update request body
            await fetch(updateUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': csrfToken,
                },
                body: JSON.stringify(updateData),
            });
        }
    }

    fetchFacesData(); // Refresh the table
    facesToDelete = []; // Clear the deletion array
    //alert('All face updates and deletions processed!');
}

