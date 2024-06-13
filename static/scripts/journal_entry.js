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

async function submit_entry(event){
    event.preventDefault();

    const title = document.getElementById('title');
    const mood = document.getElementById('mood');
    const color = document.getElementById('color');
    const content = document.getElementById('content');
    const error = document.getElementById('error');
    error.innerText = '';

    try
    {
        const response = await fetch('/journal', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title: title.value,
                    mood: mood.value,
                    color : color.value,
                    content : content.value
                }),
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