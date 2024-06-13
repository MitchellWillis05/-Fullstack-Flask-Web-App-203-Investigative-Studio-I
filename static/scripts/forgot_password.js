const email_error = document.getElementById('email_popup_error')
const code_error = document.getElementById('code_popup_error')

function showEmailPopup() {
      document.getElementById('popup-overlay').style.display = 'flex';
      document.getElementById('email-popup').style.display = 'block';
      document.getElementById('code-popup').style.display = 'none';
}

async function submit_email(){
    const form = document.getElementById('email-form')
    const formData = new FormData(form);
    const error = document.getElementById('email_popup_error');
    const submitButton = document.getElementById('email-submit');
    const esubmit = document.getElementById('email-submit')
    const email = document.getElementById('email-input')
    esubmit.innerText = "Sending"
    submitButton.disabled = true;
    submitButton.classList.add('loading');
    submitButton.classList.remove('popup-submit');

    try
    {
        const response = await fetch('/submit-email',
            {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
		        email_error.innerText = '';
                alert('Confirmation code successfully sent to ' + email.value);
                document.getElementById('email-popup').style.display = 'none';
                document.getElementById('code-popup').style.display = 'block';
            }
            else if (response.status === 429) {
                const result = await response.json();
                email_error.innerText = (result.message || 'Failed to submit email.')
                startTimer(result.remaining_time);
            }
            else {
                const result = await response.json();

                error.innerText = result.message || 'Failed to login.';
            }
            esubmit.innerText = "Send"
            submitButton.disabled = false;
            submitButton.classList.remove('loading');
            submitButton.classList.add('popup-submit');
    }

    catch (error)
    {
        console.error('Error submitting entry:', error);
        error.innerText = 'An error occurred, please try again.';
    }
}


async function submitCode() {
    const form = document.getElementById('code-form')
    const formData = new FormData(form);
    const error = document.getElementById('code_popup_error');
  const code = document.getElementById('code-input').value;
  if (code) {

      try {
          const response = await fetch('/submit-code', {
                method: 'POST',
                body: formData
            });

          const result = await response.json();
          if (response.ok) {
              closePopup();
              window.location.href = '/reset-password'
          } else {
              code_error.innerText = (result.message || 'Failed to submit code.')
          }
      }
      catch (error) {
          console.error('Error submitting code:', error);
          code_error.innerText = 'An error occurred, please try again'
      }
  }
  else
  {
    code_error.innerText = 'Please enter your code'
  }
}

function closePopup() {
    document.getElementById('popup-overlay').style.display = 'none';
    document.getElementById('email-input').value = '';
    document.getElementById('code-input').value = '';
}

function stopPropagation(event) {
    event.stopPropagation();
}

function startTimer(seconds) {
    let timer = seconds, minutes, remainingSeconds;
    const timerElement = document.getElementById('timer');

    const interval = setInterval(() => {
        minutes = parseInt(timer / 60, 10);
        remainingSeconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        remainingSeconds = remainingSeconds < 10 ? "0" + remainingSeconds : remainingSeconds;

        timerElement.textContent = minutes + ":" + remainingSeconds;

        if (timer <= 0) {
            clearInterval(interval);
            timerElement.textContent = '';
            email_error.innerText = '';
        } else {
            --timer;
        }
    }, 1000);
}