async function delete_entry() {
    const form = document.getElementById('entry_id_form')
    const formData = new FormData(form);
    const error = document.getElementById('error');

    try {
        const response = await fetch('/delete-entry', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            error.innerText = "";
            window.location.href = '/journal';
        } else {
            const result = await response.json();
            error.innerText = result.message || 'Failed to delete entry.';
        }
    } catch (error) {
        console.error('Error deleting entry:', error);
        error.innerText = 'An error occurred, please try again.';
    }
}


async function generate_response() {
    const id = document.getElementById('entry_id');
    const error = document.getElementById('error');
    const ai_response = document.getElementById('ai_response');
    const submitButton = document.getElementById('generate-button');
    error.innerText = "";
    submitButton.disabled = true;
    submitButton.classList.add('journal-add-entry-btn-loading');
    submitButton.classList.remove('journal-add-entry-btn');
    try {
        const response = await fetch('/entry/' + id.value, {
            method: 'POST'
        });

        if (response.ok) {
            const result = await response.json();
            error.innerText = "";
            displayTextOneLetterAtATime(result.message, ai_response);
        } else {
            const result = await response.json();
            error.innerText = result.message || 'Failed to generate response.';
        }
    } catch (error) {
        console.error('Error generating response:', error);
        error.innerText = 'An error occurred, please try again.';
    }
    submitButton.disabled = false;
    submitButton.classList.remove('journal-add-entry-btn-loading');
    submitButton.classList.add('journal-add-entry-btn');
}

function displayTextOneLetterAtATime(text, element) {
    element.innerText = ''; // Clear any existing text
    let index = 0;

    function addNextLetter() {
        if (index < text.length) {
            // Create a text node for the next character
            const charNode = document.createTextNode(text[index]);
            element.appendChild(charNode);
            index++;
            setTimeout(addNextLetter, 50); // Adjust the delay as needed (50ms in this case)
        }
    }

    addNextLetter();
}

