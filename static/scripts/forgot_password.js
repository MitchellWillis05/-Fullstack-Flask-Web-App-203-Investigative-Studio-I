const validateEmail = (email) => {
  return String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
};

const email_error = document.getElementById('email_popup_error')
const code_error = document.getElementById('code_popup_error')

function showEmailPopup() {
      document.getElementById('popup-overlay').style.display = 'flex';
      document.getElementById('email-popup').style.display = 'block';
      document.getElementById('code-popup').style.display = 'none';
    }

async function submitEmail(event) {
    event.preventDefault();
    const submitButton = document.getElementById('email-submit');
    const esubmit = document.getElementById('email-submit')
    esubmit.innerText = "Sending"
    submitButton.disabled = true;
    submitButton.classList.add('loading');
    submitButton.classList.remove('popup-submit');
    const email = document.getElementById('email-input').value;
    if (email && validateEmail(email))
    {
        try
        {
            const response = await fetch('/submit-email', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email }),
            });
            const result = await response.json();
            if (response.ok) {
                email_error.innerText = '';
                alert('Confirmation code successfully sent to ' + email);
                document.getElementById('email-popup').style.display = 'none';
                document.getElementById('code-popup').style.display = 'block';
            }
            else if (response.status === 429) {
                email_error.innerText = (result.message || 'Failed to submit email.')
                startTimer(result.remaining_time);
            }
            else
            {
                email_error.innerText = (result.message || 'Failed to submit email.')
            }
        }
        catch (error)
        {
            console.error('Error submitting email:', error);
            email_error.innerText = ('Error, failed to submit email.')
        }
    }
    else if (email === '' || email == null)
    {
        email_error.innerText = ('Please enter your email.')
    }
    else if (!validateEmail(email))
    {
        email_error.innerText = ('Error, invalid email.')
    }
    esubmit.innerText = "Send"
    submitButton.disabled = false;
    submitButton.classList.remove('loading');
    submitButton.classList.add('popup-submit');
}

async function submitCode(event) {
  event.preventDefault();
  const code = document.getElementById('code-input').value;
  if (code) {

      try {
          const response = await fetch('/submit-code', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({code: code}),
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