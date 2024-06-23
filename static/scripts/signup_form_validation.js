const code_popup_error = document.getElementById('code_popup_error');
async function submit_entry(){

    const error = document.getElementById('error');
    const form = document.getElementById('signup');
    const formData = new FormData(form);
    const submitButton = document.getElementById('sign-up-btn');
    submitButton.innerText = "Please wait..."
    submitButton.disabled = true;
    submitButton.classList.add('loading');
    try
    {
        const response_a = await fetch('/submit-signup-email',
            {
                method: 'POST',
                body: formData
            });

            if (response_a.ok) {
                const result = await response_a.json();
                console.log("Validation successful.")
                showEmailPopup()
            }
            else if (response_a.status === 429) {
                const result = await response_a.json();
                code_popup_error.innerText = (result.message || 'Please wait before sending another email.')
                showEmailPopup();
                startTimer(result.remaining_time);
            }
            else {
                const result = await response_a.json();

                error.innerText = result.message || 'Failed to signup.';
            }
    }

    catch (error)
    {
        console.error('Error submitting entry:', error);
        error.innerText = 'An error occurred, please try again.';
    }
    submitButton.innerText = "Sign Up"
    submitButton.disabled = false;
    submitButton.classList.remove('loading');
}

async function submitCode() {
    const form = document.getElementById('code-form')
    const formData = new FormData(form);
    const code = document.getElementById('code-input').value;

  if (code) {

      try {
          const response = await fetch('/submit-code', {
                method: 'POST',
                body: formData
            });

          const result = await response.json();
          if (response.ok) {
              await create_user();
          } else {
              code_popup_error.innerText = (result.message || 'Failed to submit code.')
          }
      }
      catch (error) {
          console.error('Error submitting code:', error);
          code_popup_error.innerText = 'An error occurred, please try again'
      }
  }
  else
  {
    code_popup_error.innerText = 'Please enter your code'
  }
}

async function create_user(){
    const error = document.getElementById('error');
    const form = document.getElementById('signup');
    const formData = new FormData(form);
    try
    {
        const response_b = await fetch('/signup',
            {
                method: 'POST',
                body: formData
            });

            if (response_b.ok) {
                const result = await response_b.json();
                alert("Account successfully created.")
                window.location.href = '/login';
            } else {
                const result = await response_b.json();

                code_popup_error.innerText = result.message || 'Failed to signup.';
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
      document.getElementById('code-popup').style.display = 'block';
}

function closePopup() {
    document.getElementById('popup-overlay').style.display = 'none';
    document.getElementById('email-input').value = '';
    document.getElementById('code-input').value = '';
}

function updateGender() {
    const genderSelect = document.getElementById('gender');
    document.getElementById('selected-gender').value = genderSelect.options[genderSelect.selectedIndex].value;
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
            code_popup_error.innerText = '';
        } else {
            --timer;
        }
    }, 1000);
}

function stopPropagation(event) {
    event.stopPropagation();
}


