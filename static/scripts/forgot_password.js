const validateEmail = (email) => {
  return String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
};


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
                alert('Confirmation code successfully sent to ' + email);
                document.getElementById('email-popup').style.display = 'none';
                document.getElementById('code-popup').style.display = 'block';
            }
            else
            {
                alert(result.message || 'Failed to submit email.');
            }
        }
        catch (error)
        {
            console.error('Error submitting email:', error);
            alert('An error occurred. Please try again.');
        }
    }
    else if (email === '' || email == null)
    {
        alert('Please enter your email.');
    }
    else if (!validateEmail(email))
    {
        alert('Invalid email');
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
              alert('Code submitted successfully.');
              closePopup();
          } else {
              alert(result.message || 'Failed to submit code.');
          }
      }
      catch (error) {
          console.error('Error submitting code:', error);
          alert('An error occurred. Please try again.');
      }
  }
  else {
    alert('Please enter the code.');
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
