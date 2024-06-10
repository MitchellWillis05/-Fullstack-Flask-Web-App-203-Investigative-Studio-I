const form = document.getElementById('reset_password');
const errorElement = document.getElementById('error');

function show_success_popup() {
    document.getElementById('popup-overlay').style.display = 'flex';
    document.getElementById('confirm-popup').style.display = 'block';
}

function validatePassword(password, confirmPassword, errorElement) {
    errorElement.innerText = '';

    if (password.value === '' || password.value == null) {
        errorElement.innerText = 'Password is required';
        return false;
    }

    if (confirmPassword.value === '' || confirmPassword.value == null) {
        errorElement.innerText = 'Please confirm password';
        return false;
    }

    if (password.value.length < 10) {
        errorElement.innerText = 'Password must be 10 characters or longer';
        return false;
    }

    if (password.value !== confirmPassword.value) {
        errorElement.innerText = 'Passwords do not match';
        return false;
    }

    return true;
}

function closeSubmit() {
    document.getElementById('popup-overlay').style.display = 'none';
    window.location.href = '/login';
}

async function submitPassword(event) {
    event.preventDefault();

    const password = document.getElementById('password');
    const confirm_password = document.getElementById('confirm_password');
    const error = document.getElementById('error');
    const code_error = document.getElementById('code_error');

    if (validatePassword(password, confirm_password, error)) {
        try {
            const response = await fetch('/reset-password-redirect', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    password: password.value,
                    confirm_password: confirm_password.value
                }),
            });

            if (response.ok) {
                const result = await response.json();
                show_success_popup();
            } else {
                const result = await response.json();
                error.innerText = result.message || 'Failed to update password.';
            }
        } catch (error) {
            console.error('Error updating password:', error);
            error.innerText = 'An error occurred, please try again.';
        }
    } else {
        code_error.innerText = 'Please enter a valid password.';
    }
}

form.addEventListener('submit', submitPassword);
