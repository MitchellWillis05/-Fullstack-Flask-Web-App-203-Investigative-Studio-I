
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
                window.location.href = '/';
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
