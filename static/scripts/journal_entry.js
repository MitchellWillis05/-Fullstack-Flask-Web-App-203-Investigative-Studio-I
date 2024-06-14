
function openForm()
{
    document.getElementById("newEntryForm").style.display = "block";
}

function closeForm()
{
    document.getElementById("newEntryForm").style.display = "none";
    document.getElementById('title').value = "";
    document.getElementById('mood').value = "";
    document.querySelectorAll('.journal-mood-btn').forEach(btn => btn.classList.remove('selected'));
    document.getElementById('color').value = "";
    document.querySelectorAll('.journal-color-btn').forEach(btn => btn.classList.remove('selected'));
    document.getElementById('content').value = "";
    document.getElementById('error').value = "";
}

function selectMood(button, emotion)
{
    document.querySelectorAll('.journal-mood-btn').forEach(btn => btn.classList.remove('selected'));
    button.classList.add('selected');
    document.getElementById('mood').value = emotion;
}

function selectColor(button, color)
{
    document.querySelectorAll('.journal-color-btn').forEach(btn => btn.classList.remove('selected'));
    button.classList.add('selected');
    document.getElementById('color').value = color;
}

async function submit_entry(){
    const form = document.getElementById('entry-form')
    const formData = new FormData(form);
    const error = document.getElementById('error');

    try
    {
        const response = await fetch('/journal', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                window.location.href = '/journal';
            } else {
                const result = await response.json();
                error.innerText = result.message || 'Failed to submit entry.';
            }


    }

    catch (error)
    {
        console.error('Error submitting entry:', error);
        error.innerText = 'An error occurred, please try again.';
    }

}