// Load notes when the page opens
document.addEventListener("DOMContentLoaded", loadNotes);

function loadNotes() {
    fetch("/notes")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("notes-container");
            container.innerHTML = "";
            data.forEach(note => {
                const div = document.createElement("div");
                div.className = "note";
                div.innerHTML = `
                    <h3>${note.title}</h3>
                    <p>${note.content}</p>
                    <small>${note.created_at}</small><br>
                    <button onclick="deleteNote(${note.id})">Delete</button>
                    <button onclick="editNote(${note.id}, '${note.title}', '${note.content}')">Edit</button>
                `;
                container.appendChild(div);
            });
        });
}

function addNote() {
    const title = document.getElementById("title").value;
    const content = document.getElementById("content").value;

    if (!title || !content) {
        alert("Please enter title and content");
        return;
    }

    fetch("/add_note", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ title, content })
    })
    .then(response => response.json())
    .then(() => {
        document.getElementById("title").value = "";
        document.getElementById("content").value = "";
        loadNotes();
    });
}

function deleteNote(id) {
    fetch(`/delete_note/${id}`, { method: "DELETE" })
        .then(response => response.json())
        .then(() => loadNotes());
}

function editNote(id, oldTitle, oldContent) {
    const newTitle = prompt("Edit Title:", oldTitle);
    const newContent = prompt("Edit Content:", oldContent);

    if (newTitle && newContent) {
        fetch(`/update_note/${id}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ title: newTitle, content: newContent })
        })
        .then(response => response.json())
        .then(() => loadNotes());
    }
}



