// Smooth Delete Animation
document.querySelectorAll(".delete-btn").forEach(btn => {
    btn.addEventListener("click", function (e) {
        e.preventDefault();
        const target = this.closest(".card");
        target.classList.add("fade-out");
        setTimeout(() => {
            target.remove(); // Remove element from DOM after fade-out
        }, 500);
    });
});

// Drag and Drop Upload
const dropArea = document.querySelector("#drop-area");
dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.classList.add("drag-over");
});

dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("drag-over");
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove("drag-over");
    const files = e.dataTransfer.files;
    handleFileUpload(files); // Function to handle file uploads
});

function handleFileUpload(files) {
    // Display a loading spinner
    const spinner = document.createElement("div");
    spinner.classList.add("spinner");
    document.body.appendChild(spinner);

    // Simulate upload delay for demo
    setTimeout(() => {
        spinner.remove();
        alert("Files uploaded successfully!");
    }, 2000);
}

// Trash Restore Countdown Timer
document.querySelectorAll(".trash-timer").forEach(timer => {
    const deadline = new Date(timer.dataset.deadline);
    const interval = setInterval(() => {
        const now = new Date();
        const remaining = Math.max(deadline - now, 0);

        if (remaining === 0) {
            clearInterval(interval);
            timer.innerText = "Expired";
        } else {
            const hours = Math.floor((remaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((remaining % (1000 * 60 * 60)) / (1000 * 60));
            timer.innerText = `${hours}h ${minutes}m remaining`;
        }
    }, 1000);
});


// Attach event listener to delete buttons
document.querySelectorAll(".delete-btn").forEach(btn => {
    btn.addEventListener("click", function (e) {
        e.preventDefault(); // Prevent the default link behavior
        const folderId = this.dataset.folderId; // Get the folder ID

        // Send AJAX POST request to delete the folder
        fetch(`/ajax/delete-folder/${folderId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token for security
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json()) // Handle the JSON response
        .then(data => {
            if (data.success) {
                // Remove folder card dynamically from the DOM
                const folderCard = this.closest(".card");
                folderCard.remove();
                showMessage(data.message, "success");
            } else {
                showMessage(data.message, "error");
            }
        })
        .catch(error => {
            console.error("Error deleting folder:", error);
            showMessage("An error occurred. Please try again.", "error");
        });
    });
});

// Function to show success/error messages dynamically
function showMessage(message, type) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `alert alert-${type}`;
    msgDiv.innerText = message;
    document.body.prepend(msgDiv);
    setTimeout(() => msgDiv.remove(), 3000);
}

// CSRF Token Helper Function
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split("; ");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i];
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.split("=")[1]);
                break;
            }
        }
    }
    return cookieValue;
}
// Rename folder functionality
document.querySelectorAll(".rename-btn").forEach(btn => {
    btn.addEventListener("click", function (e) {
        e.preventDefault(); // Prevent the default link behavior
        const folderId = this.dataset.folderId; // Get the folder ID
        const oldName = this.dataset.folderName; // Get the current folder name

        // Prompt user for new folder name
        const newName = prompt("Enter new folder name:", oldName);

        if (newName && newName !== oldName) {
            // Send AJAX POST request to rename the folder
            fetch(`/ajax/rename-folder/${folderId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token for security
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ new_name: newName })
            })
            .then(response => response.json()) // Handle the JSON response
            .then(data => {
                if (data.success) {
                    // Update folder name dynamically in the DOM
                    const folderTitle = this.closest(".card").querySelector(".card-title");
                    folderTitle.textContent = newName;
                    showMessage(data.message, "success");
                } else {
                    showMessage(data.message, "error");
                }
            })
            .catch(error => {
                console.error("Error renaming folder:", error);
                showMessage("An error occurred. Please try again.", "error");
            });
        }
    });
});
// Delete file functionality
document.querySelectorAll(".delete-file-btn").forEach(btn => {
    btn.addEventListener("click", function (e) {
        e.preventDefault(); // Prevent default behavior
        const fileId = this.dataset.fileId; // Get the file ID

        // Send AJAX POST request to delete the file
        fetch(`/ajax/delete-file/${fileId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json()) // Handle the response
        .then(data => {
            if (data.success) {
                // Remove file card dynamically
                const fileCard = this.closest(".card");
                fileCard.remove();
                showMessage(data.message, "success");
            } else {
                showMessage(data.message, "error");
            }
        })
        .catch(error => {
            console.error("Error deleting file:", error);
            showMessage("An error occurred. Please try again.", "error");
        });
    });
});

