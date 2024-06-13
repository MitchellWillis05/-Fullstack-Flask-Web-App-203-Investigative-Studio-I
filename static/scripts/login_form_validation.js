
async function submit_entry(){
    const form = document.getElementById('login')
    const formData = new FormData(form);
    const error = document.getElementById('error');

    try
    {
        const response = await fetch('/login',
            {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                window.location.href = '/';
            } else {
                const result = await response.json();

                error.innerText = result.message || 'Failed to login.';
            }
    }

    catch (error)
    {
        console.error('Error submitting entry:', error);
        error.innerText = 'An error occurred, please try again.';
    }
}
