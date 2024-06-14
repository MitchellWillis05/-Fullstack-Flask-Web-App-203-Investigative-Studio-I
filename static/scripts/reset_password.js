function show_success_popup() {
    document.getElementById('popup-overlay').style.display = 'flex';
    document.getElementById('confirm-popup').style.display = 'block';
}

function closeSubmit() {
    document.getElementById('popup-overlay').style.display = 'none';
    window.location.href = '/login';
}


async function submit_password(){
    const form = document.getElementById('reset_password')
    const formData = new FormData(form);
    const error = document.getElementById('error');

    try
    {
        const response = await fetch('/reset-password',
            {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                show_success_popup();
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

