
async function submit_entry(){
    const form = document.getElementById('signup')
    const formData = new FormData(form);
    const error = document.getElementById('error');

    try
    {
        const response = await fetch('/signup',
            {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                window.location.href = '/login';
            } else {
                const result = await response.json();

                error.innerText = result.message || 'Failed to signup.';
            }
    }

    catch (error)
    {
        console.error('Error submitting entry:', error);
        error.innerText = 'An error occurred, please try again.';
    }
}

function showEmailPopup() {
      document.getElementById('popup-overlay').style.display = 'flex';
      document.getElementById('email-popup').style.display = 'block';
      document.getElementById('code-popup').style.display = 'none';
}

function closePopup() {
    document.getElementById('popup-overlay').style.display = 'none';
    document.getElementById('email-input').value = '';
    document.getElementById('code-input').value = '';
}



function stopPropagation(event) {
    event.stopPropagation();
}


